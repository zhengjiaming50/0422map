<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="app">
    <router-view />
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
  overflow: hidden;
}

.app {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .home h1 {
    font-size: 2rem;
  }
  
  .home .subtitle {
    font-size: 1rem;
  }
}
</style>
