#!/usr/bin/env python3
"""
初始化股票数据库
从 akshare 获取 A 股列表并存入 SQLite
"""
import akshare as ak
import sqlite3
import os
from datetime import datetime


def init_stocks_db(db_path: str = None):
    """
    初始化股票数据库

    Args:
        db_path: 数据库路径，默认为当前目录下的 stocks.db
    """
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), 'stocks.db')

    print(f'数据库路径: {db_path}')
    print('正在获取 A 股列表...')

    # 获取 A 股列表
    df = ak.stock_info_a_code_name()
    print(f'获取到 {len(df)} 只股票')

    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        market TEXT,
        status TEXT DEFAULT 'active',
        updated_at TEXT
    )
    ''')

    # 清空旧数据
    cursor.execute('DELETE FROM stocks')

    # 插入数据
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for _, row in df.iterrows():
        code = row['code']
        name = row['name'].strip()

        # 判断市场：6开头是上海，0/3开头是深圳
        if code.startswith('6'):
            market = 'SH'
        else:
            market = 'SZ'

        # 判断状态：ST 股票标记
        if 'ST' in name or '*ST' in name:
            status = 'ST'
        elif name.startswith('N') or name.startswith('C'):
            status = 'NEW'  # 新股
        else:
            status = 'active'

        cursor.execute(
            'INSERT OR REPLACE INTO stocks (code, name, market, status, updated_at) VALUES (?, ?, ?, ?, ?)',
            (code, name, market, status, now)
        )

    conn.commit()

    # 统计
    cursor.execute('SELECT status, COUNT(*) FROM stocks GROUP BY status')
    stats = cursor.fetchall()
    print('\n股票状态统计:')
    for status, count in stats:
        print(f'  {status}: {count}')

    cursor.execute('SELECT COUNT(*) FROM stocks')
    total = cursor.fetchone()[0]
    print(f'\n总计: {total} 只股票')
    print(f'数据库已保存到: {db_path}')

    conn.close()
    return db_path


if __name__ == '__main__':
    init_stocks_db()
