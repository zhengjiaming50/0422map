<template>
  <div class="map-view">
    <header class="map-header">
      <h1>武汉美食地图</h1>
      <router-link to="/" class="home-link">返回首页</router-link>
    </header>
    
    <div class="map-container">
      <div class="filter-panel-container">
        <!-- 筛选面板将在这里实现 -->
        <div class="filter-placeholder">
          <h3>筛选面板</h3>
          <p>将在下一步实现筛选和搜索功能</p>
        </div>
      </div>
      
      <div class="map-wrapper">
        <div id="map" class="mapbox-container"></div>
        <div class="map-controls">
          <button class="control-btn zoom-in">+</button>
          <button class="control-btn zoom-out">-</button>
          <button class="control-btn reset">⟳</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// 临时Mapbox访问令牌，实际开发中应放在环境变量中
const mapboxToken = 'pk.eyJ1IjoiZXhhbXBsZXVzZXIiLCJhIjoiY2xoajN2aGNuMDJpYjNkbXV1ZHB6aGxjYyJ9.example'

// 地图实例
const map = ref(null)

// 初始化地图
const initMap = () => {
  // 设置Mapbox访问令牌
  mapboxgl.accessToken = mapboxToken
  
  // 创建地图实例
  map.value = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [114.3008, 30.5433], // 武汉市中心坐标
    zoom: 12
  })
  
  // 添加导航控件
  map.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
  
  // 地图加载完成事件
  map.value.on('load', () => {
    console.log('地图加载完成')
  })
}

// 组件挂载时初始化地图
onMounted(() => {
  initMap()
})

// 组件卸载时销毁地图
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
  }
})
</script>

<style scoped>
.map-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #d32f2f;
  color: white;
  padding: 1rem 2rem;
}

.map-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.home-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.map-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.filter-panel-container {
  width: 300px;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
  padding: 1rem;
  overflow-y: auto;
}

.filter-placeholder {
  padding: 1rem;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.map-wrapper {
  flex: 1;
  position: relative;
}

.mapbox-container {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  right: 20px;
  bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: white;
  border: 1px solid #ddd;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.control-btn:hover {
  background-color: #f5f5f5;
}
</style> 