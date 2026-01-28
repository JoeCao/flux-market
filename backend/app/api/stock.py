"""
股票数据 API 路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.stock import KLineResponse
from app.services.stock_service import StockService

router = APIRouter()


@router.get("/kline", response_model=KLineResponse)
async def get_kline(
    symbol: str = Query(..., description="股票代码，如 AAPL"),
    start_date: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
    adjust: str = Query("qfq", description="复权类型：qfq(前复权)/hfq(后复权)/空字符串(不复权)")
):
    """
    获取股票K线数据

    - **symbol**: 股票代码（必填），如 AAPL、TSLA、GOOGL
    - **start_date**: 开始日期（可选），默认为30天前
    - **end_date**: 结束日期（可选），默认为今天
    - **adjust**: 复权类型（可选），默认为前复权(qfq)
    """
    try:
        data = StockService.get_stock_kline(
            symbol=symbol.upper(),
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )

        return KLineResponse(
            code=0,
            message="success",
            data=data
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.get("/info/{symbol}")
async def get_stock_info(symbol: str):
    """
    获取股票基本信息（预留接口）

    - **symbol**: 股票代码
    """
    return {
        "code": 0,
        "message": "success",
        "data": {
            "symbol": symbol.upper(),
            "name": f"{symbol.upper()} Stock",
            "note": "此接口为预留接口，后续可扩展更多信息"
        }
    }


@router.get("/search")
async def search_stocks(
    keyword: str = Query(..., description="搜索关键词（股票代码或名称）"),
    limit: int = Query(20, description="返回数量限制")
):
    """
    搜索股票

    - **keyword**: 搜索关键词，支持股票代码或名称模糊匹配
    - **limit**: 返回数量限制，默认20条
    """
    results = StockService.search_stocks(keyword, limit)
    return {
        "code": 0,
        "message": "success",
        "data": results
    }


@router.get("/validate/{symbol}")
async def validate_stock(symbol: str):
    """
    验证股票代码是否有效

    - **symbol**: 股票代码
    """
    valid, name, status = StockService.validate_stock_code(symbol)
    return {
        "code": 0,
        "message": "success",
        "data": {
            "valid": valid,
            "code": symbol,
            "name": name,
            "status": status
        }
    }
