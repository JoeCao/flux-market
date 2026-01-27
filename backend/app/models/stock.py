"""
股票数据模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class KLineData(BaseModel):
    """单条K线数据"""
    date: str = Field(..., description="日期")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: float = Field(..., description="成交量")


class KLineResponse(BaseModel):
    """K线数据响应"""
    code: int = Field(0, description="状态码，0表示成功")
    message: str = Field("success", description="响应消息")
    data: Optional[dict] = Field(None, description="数据内容")


class StockKLineRequest(BaseModel):
    """股票K线请求参数"""
    symbol: str = Field(..., description="股票代码，如 AAPL")
    start_date: Optional[str] = Field(None, description="开始日期，格式：YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="结束日期，格式：YYYY-MM-DD")
    adjust: str = Field("qfq", description="复权类型：qfq(前复权)/hfq(后复权)/空字符串(不复权)")
