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
          } else {
            const color = item.seriesName === 'MA5' ? '#ff6b6b' :
                         item.seriesName === 'MA10' ? '#4ecdc4' : '#ffe66d'
            result += `<div style="margin: 2px 0;">
              <span style="color: ${color};">${item.seriesName}:</span> <span style="color: #e5e7eb;">${item.data !== null ? item.data : '-'}</span>
            </div>`
          }
        })
        result += `</div>`
        return result
      }
    },
    legend: {
      data: ['K线', 'MA5', 'MA10', 'MA20', '成交量'],
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
        height: '55%',
        borderColor: '#1a1f2e'
      },
      {
        left: '3%',
        right: '3%',
        top: '72%',
        height: '18%',
        borderColor: '#1a1f2e'
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: [],
        gridIndex: 0,
        axisLine: {
          lineStyle: {
            color: '#1a1f2e'
          }
        },
        axisLabel: {
          color: '#6b7280',
          fontSize: 11,
          rotate: 30
        },
        splitLine: {
          show: false
        }
      },
      {
        type: 'category',
        data: [],
        gridIndex: 1,
        axisLine: {
          lineStyle: {
            color: '#1a1f2e'
          }
        },
        axisLabel: {
          show: false
        },
        splitLine: {
          show: false
        }
      }
    ],
    yAxis: [
      {
        scale: true,
        gridIndex: 0,
        splitNumber: 4,
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#6b7280',
          fontSize: 11
        },
        splitLine: {
          lineStyle: {
            color: '#1a1f2e',
            type: 'dashed'
          }
        }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#6b7280',
          fontSize: 11
        },
        splitLine: {
          show: false
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 0,
        end: 100
      },
      {
        show: true,
        xAxisIndex: [0, 1],
        type: 'slider',
        bottom: '2%',
        start: 0,
        end: 100,
        height: 20,
        borderColor: '#1a1f2e',
        fillerColor: 'rgba(0, 255, 136, 0.1)',
        handleStyle: {
          color: '#00ff88'
        },
        textStyle: {
          color: '#6b7280'
        },
        dataBackground: {
          lineStyle: {
            color: '#1a1f2e'
          },
          areaStyle: {
            color: '#1a1f2e'
          }
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
          color: '#00ff88',      // 涨：绿色
          color0: '#ef4444',     // 跌：红色
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
        lineStyle: {
          width: 1.5,
          color: '#ff6b6b'
        },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'MA10',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: {
          width: 1.5,
          color: '#4ecdc4'
        },
        showSymbol: false,
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        name: 'MA20',
        type: 'line',
        data: [],
        smooth: false,
        lineStyle: {
          width: 1.5,
          color: '#ffe66d'
        },
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
            if (!props.data) return '#00ff88'
            const klineData = props.data.kline[dataIndex]
            // 涨绿跌红
            return klineData[1] >= klineData[0] ? '#00ff88' : '#ef4444'
          },
          opacity: 0.6
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

// 更新图表数据
const updateChart = () => {
  if (!chartInstance || !props.data) return

  chartInstance.setOption({
    title: {
      text: `${props.data.symbol} 股票K线图`
    },
    xAxis: [
      {
        data: props.data.dates
      },
      {
        data: props.data.dates
      }
    ],
    series: [
      {
        data: props.data.kline
      },
      {
        data: props.data.ma5
      },
      {
        data: props.data.ma10
      },
      {
        data: props.data.ma20
      },
      {
        data: props.data.volumes
      }
    ]
  })
}

// 监听数据变化
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

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
