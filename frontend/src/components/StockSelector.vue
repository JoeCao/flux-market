<template>
  <div class="stock-selector">
    <div class="selector-form">
      <div class="form-row">
        <div class="form-item">
          <label>股票代码:</label>
          <input
            v-model="formData.symbol"
            type="text"
            placeholder="如: AAPL, 000001, 600000"
            @keyup.enter="handleQuery"
          />
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
import { reactive, ref } from 'vue'
import type { StockQueryParams } from '../types/stock'

// Emits
const emit = defineEmits<{
  query: [params: StockQueryParams]
}>()

// Props
defineProps<{
  loading?: boolean
  error?: string
}>()

// 表单数据
const formData = reactive<StockQueryParams>({
  symbol: 'AAPL',
  start_date: '',
  end_date: '',
  adjust: 'qfq'
})

// 查询处理
const handleQuery = () => {
  if (!formData.symbol) return

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
