<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div id="app">
    <div class="cyber-backdrop"></div>
    <div class="cyber-grid"></div>
    <div class="cyber-scanline"></div>
    <div class="cyber-glitch-overlay"></div>
    <router-view></router-view>
  </div>
</template>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', sans-serif;
  background-color: #f8f8f8;
  color: #333;
  line-height: 1.6;
  overflow-x: hidden; /* 只隐藏水平滚动条 */
  overflow-y: auto; /* 允许垂直滚动 */
}

.app {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow-x: hidden; /* 只隐藏水平滚动条 */
  overflow-y: auto; /* 允许垂直滚动 */
}

#app {
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.cyber-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--cp-darker);
  z-index: -10;
}

.cyber-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(0deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  background-position: -1px -1px;
  z-index: -5;
  pointer-events: none;
}

.cyber-scanline {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(
    to bottom,
    transparent 50%,
    rgba(5, 217, 232, 0.05) 51%
  );
  background-size: 100% 4px;
  pointer-events: none;
  z-index: 100;
  opacity: 0.4;
}

.cyber-glitch-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 101;
  opacity: 0.2;
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAMAAAADCAYAAABWKLW/AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkI5QzJDRDU5NzM4MTExRUFCODZCOTk3MkNDMEEwQ0RFIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkI5QzJDRDVBNzM4MTExRUFCODZCOTk3MkNDMEEwQ0RFIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6QjlDMkNENTc3MzgxMTFFQUI4NkI5OTcyQ0MwQTBDREUiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6QjlDMkNENTg3MzgxMTFFQUI4NkI5OTcyQ0MwQTBDREUiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6cv/EQAAAAH0lEQVR42mL8z8DwnwEJMDKBCEYGRgYmBjwAIMAA3xsEMGN0S/sAAAAASUVORK5CYII=');
  animation: glitch 2s infinite;
}

@keyframes glitch {
  0% {
    opacity: 0;
  }
  25% {
    opacity: 0.05;
    transform: translate(1px, 3px);
  }
  50% {
    opacity: 0;
  }
  75% {
    opacity: 0.05;
    transform: translate(-2px, -2px);
  }
  100% {
    opacity: 0;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .home h1 {
    font-size: 2rem;
  }
  
  .home .subtitle {
    font-size: 1rem;
  }

  .cyber-grid {
    background-size: 20px 20px;
  }
}
</style>
