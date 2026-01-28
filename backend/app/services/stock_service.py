"""
股票数据服务
封装 akshare 调用，处理数据格式化和均线计算
"""
import akshare as ak
import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple


class StockService:
    """股票数据服务类"""

    # 数据库路径
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'stocks.db')

    @staticmethod
    def validate_stock_code(symbol: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        验证股票代码是否有效

        Args:
            symbol: 6位股票代码

        Returns:
            (是否有效, 股票名称, 状态)
        """
        try:
            conn = sqlite3.connect(StockService.DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT name, status FROM stocks WHERE code = ?', (symbol,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return True, result[0], result[1]
            return False, None, None
        except Exception:
            # 数据库不存在或查询失败，跳过验证
            return True, None, None

    @staticmethod
    def search_stocks(keyword: str, limit: int = 20) -> List[Dict]:
        """
        搜索股票

        Args:
            keyword: 搜索关键词（代码或名称）
            limit: 返回数量限制

        Returns:
            匹配的股票列表
        """
        try:
            conn = sqlite3.connect(StockService.DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT code, name, market, status FROM stocks
                WHERE code LIKE ? OR name LIKE ?
                LIMIT ?
            ''', (f'%{keyword}%', f'%{keyword}%', limit))
            results = cursor.fetchall()
            conn.close()

            return [
                {'code': r[0], 'name': r[1], 'market': r[2], 'status': r[3]}
                for r in results
            ]
        except Exception:
            return []

    @staticmethod
    def calculate_ma(data: pd.Series, period: int) -> List[Optional[float]]:
        """
        计算移动平均线

        Args:
            data: 收盘价序列
            period: 周期

        Returns:
            移动平均线数据列表
        """
        ma = data.rolling(window=period).mean()
        return [None if pd.isna(x) else round(float(x), 2) for x in ma]

    @staticmethod
    def get_stock_kline(
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjust: str = "qfq"
    ) -> Dict:
        """
        获取股票K线数据（支持美股和A股）

        Args:
            symbol: 股票代码
                - 美股: AAPL, TSLA 等
                - A股: 000001, 600000 等（6位数字）
            start_date: 开始日期，格式 YYYY-MM-DD
            end_date: 结束日期，格式 YYYY-MM-DD
            adjust: 复权类型，qfq/hfq/空字符串

        Returns:
            包含K线数据和均线的字典
        """
        try:
            # 判断是A股还是美股
            is_a_stock = symbol.isdigit() and len(symbol) == 6

            if is_a_stock:
                # 验证股票代码
                valid, name, status = StockService.validate_stock_code(symbol)
                if not valid:
                    raise ValueError(f"股票代码 {symbol} 不存在，请检查代码是否正确")

                # A股数据
                df = StockService._get_a_stock_data(symbol, adjust)
            else:
                # 美股数据
                df = ak.stock_us_daily(symbol=symbol, adjust=adjust)

            if df.empty:
                raise ValueError(f"未找到股票 {symbol} 的数据")

            # 设置日期索引
            df = df.set_index("date")
            df.index = pd.to_datetime(df.index)

            # 处理日期范围
            if start_date is None:
                # 默认最近90天，确保MA20有足够数据
                start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")

            # 筛选日期范围
            df = df[start_date:end_date]

            if df.empty:
                raise ValueError(f"指定日期范围内没有数据")

            # 计算均线
            ma5 = StockService.calculate_ma(df['close'], 5)
            ma10 = StockService.calculate_ma(df['close'], 10)
            ma20 = StockService.calculate_ma(df['close'], 20)

            # 格式化数据
            dates = [d.strftime("%Y-%m-%d") for d in df.index]

            # K线数据格式：[open, close, low, high] (ECharts candlestick 格式)
            kline_data = [
                [
                    round(float(row['open']), 2),
                    round(float(row['close']), 2),
                    round(float(row['low']), 2),
                    round(float(row['high']), 2)
                ]
                for _, row in df.iterrows()
            ]

            # 成交量数据
            volumes = [round(float(v), 0) for v in df['volume']]

            return {
                "symbol": symbol,
                "dates": dates,
                "kline": kline_data,
                "volumes": volumes,
                "ma5": ma5,
                "ma10": ma10,
                "ma20": ma20,
                "count": len(dates)
            }

        except Exception as e:
            raise Exception(f"获取股票数据失败: {str(e)}")

    @staticmethod
    def _get_a_stock_data(symbol: str, adjust: str = "qfq") -> pd.DataFrame:
        """
        获取A股数据（带重试机制）
        使用新浪数据源 stock_zh_a_daily，比东方财富数据源更稳定

        Args:
            symbol: 6位股票代码
            adjust: 复权类型

        Returns:
            包含K线数据的DataFrame
        """
        import time

        max_retries = 3
        retry_delay = 2

        # 转换股票代码格式：600000 -> sh600000, 000001 -> sz000001
        if symbol.startswith('6'):
            full_symbol = f"sh{symbol}"
        else:
            full_symbol = f"sz{symbol}"

        for attempt in range(max_retries):
            try:
                # 使用新浪数据源 stock_zh_a_daily（更稳定）
                df = ak.stock_zh_a_daily(symbol=full_symbol, adjust=adjust)

                # 只保留需要的列（新浪数据源列名已经是英文）
                df = df[['date', 'open', 'close', 'high', 'low', 'volume']]

                return df

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"获取A股数据失败，{retry_delay}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"获取A股数据失败（已重试{max_retries}次）: {str(e)}")
