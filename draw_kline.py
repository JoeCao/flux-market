import akshare as ak
import mplfinance as mpf
from datetime import datetime, timedelta

# 获取苹果股票数据
print("正在获取 AAPL 股票数据...")
stock_us_daily_df = ak.stock_us_daily(symbol="TSLA", adjust="qfq")

# 设置日期索引
stock_us_daily_df = stock_us_daily_df.set_index(["date"])

# 获取最近一个月的数据
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

print(f"绘制 {start_date_str} 到 {end_date_str} 的数据")
stock_us_daily_df = stock_us_daily_df[start_date_str:end_date_str]

print(f"数据行数: {len(stock_us_daily_df)}")
print("\n最新几天的数据:")
print(stock_us_daily_df.tail())

# 绘制 K 线图
print("\n正在绘制 K 线图...")
mpf.plot(
    stock_us_daily_df,
    type="candle",  # 蜡烛图
    mav=(5, 10, 20),  # 5日、10日、20日均线
    volume=True,  # 显示成交量
    show_nontrading=False,  # 不显示非交易日
    title="AAPL Stock - Last 30 Days",
    style="charles"  # 使用 charles 风格
)
