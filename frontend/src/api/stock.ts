/**
 * 股票数据 API 调用模块
 */
import axios from 'axios'
import type { ApiResponse, KLineData, StockQueryParams } from '../types/stock'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 获取股票K线数据
 */
export const getStockKLine = async (params: StockQueryParams): Promise<ApiResponse<KLineData>> => {
  return apiClient.get('/stock/kline', { params })
}

/**
 * 获取股票基本信息
 */
export const getStockInfo = async (symbol: string): Promise<ApiResponse> => {
  return apiClient.get(`/stock/info/${symbol}`)
}

export default {
  getStockKLine,
  getStockInfo
}
