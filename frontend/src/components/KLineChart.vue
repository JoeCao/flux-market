<template>
  <div ref="chartRef" :style="{ width: '100%', height: height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import type { KLineData } from '../types/stock'

// Props
const props = defineProps<{
  data: KLineData | null
  height?: string
  indicator?: 'macd' | 'kdj' | 'rsi'
}>()

// Refs
const chartRef = ref<HTMLDivElement>()
let chartInstance: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value, 'dark')

  // 设置专业股票软件风格配置
  const option: echarts.EChartsOption = {
    backgroundColor: '#0f1419',
    title: {
      text: '股票K线图',
      left: 20,
      top: 10,
      textStyle: {
        color: '#00ff88',
        fontSize: 16,
        fontWeight: 600
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        lineStyle: {
          color: '#6b7280',
          type: 'dashed'
        }
      },
      backgroundColor: 'rgba(15, 20, 25, 0.95)',
      borderColor: '#1a1f2e',
      borderWidth: 1,
      textStyle: {
        color: '#e5e7eb',
        fontSize: 12
      },
      formatter: function(params: any) {
        let result = `<div style="padding: 5px;">`
        result += `<div style="color: #00ff88; font-weight: 600; margin-bottom: 8px;">${params[0].axisValue}</div>`

        params.forEach((item: any) => {
          if (item.seriesName === 'K线') {
            const data = item.data
            const isRise = data[1] >= data[0]
            const color = isRise ? '#00ff88' : '#ef4444'
            result += `<div style="margin: 4px 0;">
              <span style="color: #6b7280;">开盘:</span> <span style="color: ${color};">${data[0]}</span>
              <span style="color: #6b7280; margin-left: 10px;">收盘:</span> <span style="color: ${color};">${data[1]}</span><br/>
              <span style="color: #6b7280;">最低:</span> <span style="color: ${color};">${data[2]}</span>
              <span style="color: #6b7280; margin-left: 10px;">最高:</span> <span style="color: ${color};">${data[3]}</span>
            </div>`
          } else if (item.seriesName === '成交量') {
            result += `<div style="margin: 4px 0;">
              <span style="color: #6b7280;">成交量:</span> <span style="color: #00bfff;">${item.data.toLocaleString()}</span>
            </div>`
          } else if (item.seriesName === 'MA5') {
            result += `<div style="margin: 2px 0;"><span style="color: #ff6b6b;">MA5:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'MA10') {
            result += `<div style="margin: 2px 0;"><span style="color: #4ecdc4;">MA10:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'MA20') {
            result += `<div style="margin: 2px 0;"><span style="color: #ffe66d;">MA20:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'BOLL上轨') {
            result += `<div style="margin: 2px 0;"><span style="color: #f472b6;">BOLL上:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'BOLL中轨') {
            result += `<div style="margin: 2px 0;"><span style="color: #a78bfa;">BOLL中:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'BOLL下轨') {
            result += `<div style="margin: 2px 0;"><span style="color: #60a5fa;">BOLL下:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'DIF') {
            result += `<div style="margin: 2px 0;"><span style="color: #fbbf24;">DIF:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'DEA') {
            result += `<div style="margin: 2px 0;"><span style="color: #34d399;">DEA:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'MACD') {
            result += `<div style="margin: 2px 0;"><span style="color: #f87171;">MACD:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'K') {
            result += `<div style="margin: 2px 0;"><span style="color: #fbbf24;">K:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'D') {
            result += `<div style="margin: 2px 0;"><span style="color: #34d399;">D:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'J') {
            result += `<div style="margin: 2px 0;"><span style="color: #f472b6;">J:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          } else if (item.seriesName === 'RSI') {
            result += `<div style="margin: 2px 0;"><span style="color: #a78bfa;">RSI:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span></div>`
          }
        })
        result += `</div>`
        return result
      }
    },
    legend: {
      data: ['K线', 'MA5', 'MA10', 'MA20', 'BOLL上轨', 'BOLL中轨', 'BOLL下轨', '成交量'],
      top: 10,
      right: 20,
      textStyle: {
        color: '#6b7280',
        fontSize: 12
      },
      itemWidth: 20,
      itemHeight: 10
    },
    grid: [
      {
        left: '3%',
        right: '3%',
        top: '12%',
        height: '40%',
        borderColor: '#1a1f2e'
      },
      {
        left: '3%',
        right: '3%',
        top: '55%',
        height: '12%',
        borderColor: '#1a1f2e'
      },
      {
        left: '3%',
        right: '3%',
        top: '70%',
        height: '18%',
        borderColor: '#1a1f2e'
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: [],
        gridIndex: 0,
        axisLine: { lineStyle: { color: '#1a1f2e' } },
        axisLabel: { show: false },
        splitLine: { show: false }
      },
      {
        type: 'category',
        data: [],
        gridIndex: 1,
        axisLine: { lineStyle: { color: '#1a1f2e' } },
        axisLabel: { show: false },
        splitLine: { show: false }
      },
      {
        type: 'category',
        data: [],
        gridIndex: 2,
        axisLine: { lineStyle: { color: '#1a1f2e' } },
        axisLabel: {
          color: '#6b7280',
          fontSize: 11,
          rotate: 30
        },
        splitLine: { show: false }
      }
    ],
    yAxis: [
      {
        scale: true,
        gridIndex: 0,
        splitNumber: 4,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#6b7280', fontSize: 11 },
        splitLine: { lineStyle: { color: '#1a1f2e', type: 'dashed' } }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#6b7280', fontSize: 11 },
        splitLine: { show: false }
      },
      {
        scale: true,
        gridIndex: 2,
        splitNumber: 2,
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#6b7280', fontSize: 11 },
        splitLine: { lineStyle: { color: '#1a1f2e', type: 'dashed' } }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1, 2],
        start: 0,
        end: 100
      },
      {
        show: true,
        xAxisIndex: [0, 1, 2],
        type: 'slider',
        bottom: '2%',
        start: 0,
        end: 100,
        height: 20,
        borderColor: '#1a1f2e',
        fillerColor: 'rgba(0, 255, 136, 0.1)',
        handleStyle: { color: '#00ff88' },
        textStyle: { color: '#6b7280' },
        dataBackground: {
          lineStyle: { color: '#1a1f2e' },
          areaStyle: { color: '#1a1f2e' }
        }
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: [],
        xAxisIndex: 0,
        yAxisIndex: 0,
        itemStyle: {
          color: '#00ff88',
          color0: '#ef4444',
          borderColor: '#00ff88',
          borderColor0: '#ef4444',
          borderWidth: 1
        }
      },
      {
        name: 'MA5',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#ff6b6b' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'MA10',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#4ecdc4' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'MA20',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#ffe66d' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'BOLL上轨',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1, color: '#f472b6', type: 'dashed' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'BOLL中轨',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1, color: '#a78bfa' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'BOLL下轨',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1, color: '#60a5fa', type: 'dashed' },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: '成交量',
        type: 'bar',
        data: [],
        xAxisIndex: 1,
        yAxisIndex: 1,
        itemStyle: {
          color: function (params: any) {
            const dataIndex = params.dataIndex
            const klineArr = props.data?.kline
            const item = klineArr?.[dataIndex] as number[] | undefined
            if (!item) return '#00ff88'
            return (item[1] as number) >= (item[0] as number) ? '#00ff88' : '#ef4444'
          },
          opacity: 0.6
        }
      },
      // MACD 指标
      {
        name: 'DIF',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#fbbf24' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      },
      {
        name: 'DEA',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#34d399' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      },
      {
        name: 'MACD',
        type: 'bar',
        data: [],
        xAxisIndex: 2,
        yAxisIndex: 2,
        itemStyle: {
          color: function (params: any) {
            return params.data >= 0 ? '#ef4444' : '#00ff88'
          }
        }
      },
      // KDJ 指标
      {
        name: 'K',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#fbbf24' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      },
      {
        name: 'D',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#34d399' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      },
      {
        name: 'J',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#f472b6' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      },
      // RSI 指标
      {
        name: 'RSI',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: { width: 1.5, color: '#a78bfa' },
        showSymbol: false,
        xAxisIndex: 2,
        yAxisIndex: 2
      }
    ]
  }

  chartInstance.setOption(option)
}

// 更新图表数据
const updateChart = () => {
  if (!chartInstance || !props.data) return

  const indicator = props.indicator || 'macd'

  // 根据选择的指标显示/隐藏对应的系列
  const macdVisible = indicator === 'macd'
  const kdjVisible = indicator === 'kdj'
  const rsiVisible = indicator === 'rsi'

  // 更新图例
  const legendData = ['K线', 'MA5', 'MA10', 'MA20', 'BOLL上轨', 'BOLL中轨', 'BOLL下轨', '成交量']
  if (macdVisible) legendData.push('DIF', 'DEA', 'MACD')
  if (kdjVisible) legendData.push('K', 'D', 'J')
  if (rsiVisible) legendData.push('RSI')

  chartInstance.setOption({
    title: {
      text: `${props.data.symbol} 股票K线图`
    },
    legend: {
      data: legendData
    },
    xAxis: [
      { data: props.data.dates },
      { data: props.data.dates },
      { data: props.data.dates }
    ],
    series: [
      { data: props.data.kline },
      { data: props.data.ma5 },
      { data: props.data.ma10 },
      { data: props.data.ma20 },
      { data: props.data.boll.upper },
      { data: props.data.boll.mid },
      { data: props.data.boll.lower },
      { data: props.data.volumes },
      // MACD
      { data: macdVisible ? props.data.macd.dif : [], lineStyle: { opacity: macdVisible ? 1 : 0 } },
      { data: macdVisible ? props.data.macd.dea : [], lineStyle: { opacity: macdVisible ? 1 : 0 } },
      { data: macdVisible ? props.data.macd.macd : [] },
      // KDJ
      { data: kdjVisible ? props.data.kdj.k : [], lineStyle: { opacity: kdjVisible ? 1 : 0 } },
      { data: kdjVisible ? props.data.kdj.d : [], lineStyle: { opacity: kdjVisible ? 1 : 0 } },
      { data: kdjVisible ? props.data.kdj.j : [], lineStyle: { opacity: kdjVisible ? 1 : 0 } },
      // RSI
      { data: rsiVisible ? props.data.rsi : [], lineStyle: { opacity: rsiVisible ? 1 : 0 } }
    ]
  })
}

// 监听数据变化
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// 监听指标切换
watch(() => props.indicator, () => {
  updateChart()
})

// 监听窗口大小变化
const handleResize = () => {
  chartInstance?.resize()
}

// 生命周期
onMounted(() => {
  initChart()
  if (props.data) {
    updateChart()
  }
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
/* 组件样式 */
</style>
