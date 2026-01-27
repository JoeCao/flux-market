<script setup lang="ts">
import Dashboard from './views/Dashboard.vue'
</script>

<template>
  <Dashboard />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Courier New', monospace, sans-serif;
  background: #0a0e27;
  color: #e5e7eb;
  overflow-x: hidden;
}

#app {
  width: 100%;
  min-height: 100vh;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #0a0e27;
}

::-webkit-scrollbar-thumb {
  background: #1a1f2e;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2a2f3e;
}

/* 选择文本颜色 */
::selection {
  background: rgba(0, 255, 136, 0.3);
  color: #00ff88;
}
</style>
