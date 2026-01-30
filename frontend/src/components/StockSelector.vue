<template>
  <div class="stock-selector">
    <div class="selector-form">
      <div class="form-row">
        <div class="form-item stock-search-item">
          <label>股票代码:</label>
          <div class="stock-search-wrapper" ref="searchWrapper">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="输入代码或名称搜索"
              @input="handleSearch"
              @focus="showDropdown = true"
              @keyup.enter="handleQuery"
              class="stock-search-input"
            />
            <div v-if="showDropdown && (searchResults.length > 0 || searchKeyword)" class="stock-dropdown">
              <div v-if="searching" class="dropdown-loading">搜索中...</div>
              <template v-else>
                <div
                  v-for="stock in searchResults"
                  :key="stock.code"
                  class="dropdown-item"
                  :class="{ 'is-st': stock.status === 'ST' }"
                  @click="selectStock(stock)"
                >
                  <span class="stock-code">{{ stock.code }}</span>
                  <span class="stock-name">{{ stock.name }}</span>
                  <span class="stock-market">{{ stock.market }}</span>
                  <span v-if="stock.status === 'ST'" class="stock-status">ST</span>
                </div>
                <div v-if="searchResults.length === 0 && searchKeyword && !searching" class="dropdown-empty">
                  未找到匹配的股票
                </div>
              </template>
            </div>
          </div>
        </div>

        <div class="form-item">
          <label>开始日期:</label>
          <input
            v-model="formData.start_date"
            type="date"
          />
        </div>

        <div class="form-item">
          <label>结束日期:</label>
          <input
            v-model="formData.end_date"
            type="date"
          />
        </div>

        <div class="form-item">
          <label>复权方式:</label>
          <select v-model="formData.adjust">
            <option value="qfq">前复权</option>
            <option value="hfq">后复权</option>
            <option value="">不复权</option>
          </select>
        </div>

        <div class="form-item">
          <label>副图指标:</label>
          <select v-model="selectedIndicator" @change="handleIndicatorChange">
            <option value="macd">MACD</option>
            <option value="kdj">KDJ</option>
            <option value="rsi">RSI</option>
          </select>
        </div>

        <div class="form-item">
          <button
            @click="handleQuery"
            :disabled="loading || !formData.symbol"
            class="query-btn"
          >
            {{ loading ? '加载中...' : '查询' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, onUnmounted } from 'vue'
import type { StockQueryParams, StockInfo } from '../types/stock'
import { searchStocks } from '../api/stock'

// Emits
const emit = defineEmits<{
  query: [params: StockQueryParams]
  indicatorChange: [indicator: 'macd' | 'kdj' | 'rsi']
}>()

// Props
defineProps<{
  loading?: boolean
  error?: string
}>()

// 表单数据
const formData = reactive<StockQueryParams>({
  symbol: '',
  start_date: '',
  end_date: '',
  adjust: 'qfq'
})

// 指标选择
const selectedIndicator = ref<'macd' | 'kdj' | 'rsi'>('macd')

const handleIndicatorChange = () => {
  emit('indicatorChange', selectedIndicator.value)
}

// 搜索相关
const searchKeyword = ref('')
const searchResults = ref<StockInfo[]>([])
const showDropdown = ref(false)
const searching = ref(false)
const searchWrapper = ref<HTMLElement | null>(null)
let searchTimer: number | null = null

// 搜索处理（防抖）
const handleSearch = () => {
  if (searchTimer) {
    clearTimeout(searchTimer)
  }

  searchTimer = window.setTimeout(async () => {
    const keyword = searchKeyword.value.trim()
    if (!keyword) {
      searchResults.value = []
      return
    }

    searching.value = true
    try {
      const response = await searchStocks(keyword, 15)
      if (response.code === 0 && response.data) {
        searchResults.value = response.data
      }
    } catch (err) {
      console.error('Search error:', err)
      searchResults.value = []
    } finally {
      searching.value = false
    }
  }, 300)
}

// 选择股票
const selectStock = (stock: StockInfo) => {
  formData.symbol = stock.code
  searchKeyword.value = `${stock.code} ${stock.name}`
  showDropdown.value = false
}

// 点击外部关闭下拉框
const handleClickOutside = (event: MouseEvent) => {
  if (searchWrapper.value && !searchWrapper.value.contains(event.target as Node)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (searchTimer) {
    clearTimeout(searchTimer)
  }
})

// 查询处理
const handleQuery = () => {
  // 如果输入的是纯数字或字母，直接使用
  const keyword = searchKeyword.value.trim()
  if (!formData.symbol && keyword) {
    // 提取代码部分（空格前的内容）
    formData.symbol = keyword.split(' ')[0] || ''
  }

  if (!formData.symbol) return

  showDropdown.value = false

  emit('query', {
    symbol: formData.symbol.toUpperCase(),
    start_date: formData.start_date || undefined,
    end_date: formData.end_date || undefined,
    adjust: formData.adjust
  })
}
</script>

<style scoped>
.stock-selector {
  padding: 15px 20px;
  background: #0f1419;
  border-bottom: 1px solid #1a1f2e;
}

.selector-form {
  width: 100%;
}

.form-row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-item label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 400;
}

.form-item input,
.form-item select {
  padding: 8px 12px;
  border: 1px solid #1a1f2e;
  background: #0a0e27;
  color: #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  min-width: 150px;
  font-family: 'Courier New', monospace;
}

.form-item input:focus,
.form-item select:focus {
  outline: none;
  border-color: #00ff88;
  background: #0f1419;
}

.form-item input::placeholder {
  color: #4b5563;
}

/* 股票搜索样式 */
.stock-search-item {
  position: relative;
}

.stock-search-wrapper {
  position: relative;
}

.stock-search-input {
  width: 220px !important;
}

.stock-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  width: 320px;
  max-height: 300px;
  overflow-y: auto;
  background: #0f1419;
  border: 1px solid #1a1f2e;
  border-top: none;
  border-radius: 0 0 4px 4px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #1a1f2e;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: #1a1f2e;
}

.dropdown-item.is-st {
  opacity: 0.7;
}

.stock-code {
  font-family: 'Courier New', monospace;
  color: #00ff88;
  font-weight: 600;
  min-width: 60px;
}

.stock-name {
  color: #e5e7eb;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stock-market {
  color: #6b7280;
  font-size: 11px;
  padding: 2px 6px;
  background: #1a1f2e;
  border-radius: 3px;
}

.stock-status {
  color: #ef4444;
  font-size: 10px;
  padding: 2px 4px;
  background: rgba(239, 68, 68, 0.2);
  border-radius: 3px;
}

.dropdown-loading,
.dropdown-empty {
  padding: 15px;
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

.query-btn {
  padding: 8px 24px;
  background: #00ff88;
  color: #0a0e27;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 0.5px;
}

.query-btn:hover:not(:disabled) {
  background: #00cc6f;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 255, 136, 0.3);
}

.query-btn:disabled {
  background: #1a1f2e;
  color: #4b5563;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  margin-top: 15px;
  padding: 10px 15px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-left: 3px solid #ef4444;
  font-size: 13px;
  font-family: 'Courier New', monospace;
}
</style>
