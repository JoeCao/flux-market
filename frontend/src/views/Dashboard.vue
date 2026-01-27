<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div>
        <h1>📊 STOCK MARKET TERMINAL</h1>
        <p>Professional Trading Platform · Real-time Market Data</p>
      </div>
    </header>

    <main class="dashboard-main">
      <StockSelector
        :loading="loading"
        :error="error"
        @query="handleQuery"
      />

      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>正在加载数据...</p>
      </div>

      <div v-else-if="klineData" class="chart-container">
        <KLineChart :data="klineData" height="600px" />

        <div class="data-info">
          <div class="info-item">
            <span class="label">股票代码:</span>
            <span class="value">{{ klineData.symbol }}</span>
          </div>
          <div class="info-item">
            <span class="label">数据条数:</span>
            <span class="value">{{ klineData.count }}</span>
          </div>
          <div class="info-item">
            <span class="label">日期范围:</span>
            <span class="value">
              {{ klineData.dates[0] }} ~ {{ klineData.dates[klineData.dates.length - 1] }}
            </span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>📈 Enter stock symbol to view K-line chart</p>
        <p class="hint">Supported: US stocks (AAPL, TSLA) / A-shares (000001, 600000)</p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import StockSelector from '../components/StockSelector.vue'
import KLineChart from '../components/KLineChart.vue'
import { getStockKLine } from '../api/stock'
import type { KLineData, StockQueryParams } from '../types/stock'

// 状态
const loading = ref(false)
const error = ref('')
const klineData = ref<KLineData | null>(null)

// 查询处理
const handleQuery = async (params: StockQueryParams) => {
  loading.value = true
  error.value = ''
  klineData.value = null

  try {
    const response = await getStockKLine(params)

    if (response.code === 0 && response.data) {
      klineData.value = response.data
    } else {
      error.value = response.message || '获取数据失败'
    }
  } catch (err: any) {
    console.error('Query error:', err)
    error.value = err.response?.data?.detail || err.message || '网络请求失败，请检查后端服务是否启动'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #0a0e27;
  padding: 0;
}

.dashboard-header {
  background: #0f1419;
  border-bottom: 1px solid #1a1f2e;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dashboard-header h1 {
  font-size: 20px;
  margin: 0;
  color: #00ff88;
  font-weight: 600;
  letter-spacing: 1px;
}

.dashboard-header p {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

.dashboard-main {
  max-width: 100%;
  margin: 0;
  padding: 0;
}

.chart-container {
  background: #0f1419;
  padding: 0;
  border-top: 1px solid #1a1f2e;
}

.data-info {
  display: flex;
  gap: 40px;
  padding: 15px 20px;
  background: #0a0e27;
  border-top: 1px solid #1a1f2e;
  border-bottom: 1px solid #1a1f2e;
}

.info-item {
  display: flex;
  gap: 10px;
  align-items: center;
}

.info-item .label {
  color: #6b7280;
  font-weight: 400;
  font-size: 13px;
}

.info-item .value {
  color: #00ff88;
  font-weight: 600;
  font-size: 14px;
  font-family: 'Courier New', monospace;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
  background: #0f1419;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #1a1f2e;
  border-top: 4px solid #00ff88;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-container p {
  color: #6b7280;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: #0f1419;
  color: #6b7280;
}

.empty-state p {
  font-size: 16px;
  margin: 10px 0;
  color: #6b7280;
}

.empty-state .hint {
  font-size: 13px;
  color: #4b5563;
}
</style>
