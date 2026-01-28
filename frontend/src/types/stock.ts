/**
 * 股票数据类型定义
 */

// K线数据项
export interface KLineDataItem {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

// K线数据响应
export interface KLineData {
  symbol: string
  dates: string[]
  kline: number[][]  // [open, close, low, high]
  volumes: number[]
  ma5: (number | null)[]
  ma10: (number | null)[]
  ma20: (number | null)[]
  count: number
}

// API响应格式
export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
}

// 股票查询参数
export interface StockQueryParams {
  symbol: string
  start_date?: string
  end_date?: string
  adjust?: 'qfq' | 'hfq' | ''
}

// 股票信息
export interface StockInfo {
  code: string
  name: string
  market: string
  status: string
}
