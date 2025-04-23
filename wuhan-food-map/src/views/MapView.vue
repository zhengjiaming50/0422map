<template>
  <div class="map-view">
    <header class="map-header">
      <h1>武汉美食地图</h1>
      <router-link to="/" class="home-link">返回首页</router-link>
    </header>
    
    <div class="map-content">
      <div class="filter-panel-container">
        <!-- 筛选面板将在下一步实现 -->
        <div class="filter-placeholder">
          <h3>筛选面板</h3>
          <p>将在下一步实现筛选和搜索功能</p>
        </div>
      </div>
      
      <div class="map-wrapper">
        <MapContainer 
          :initial-center="[114.3008, 30.5433]" 
          :initial-zoom="12"
          @map-loaded="handleMapLoaded"
          @map-click="handleMapClick"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MapContainer from '../components/MapContainer.vue'

// 地图实例
const mapInstance = ref(null)

// 地图加载完成处理
const handleMapLoaded = (map) => {
  console.log('地图在MapView中加载完成')
  mapInstance.value = map
}

// 地图点击事件处理
const handleMapClick = (e) => {
  console.log('地图点击坐标:', e.lngLat)
}
</script>

<style scoped>
.map-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #e63946;
  color: white;
  padding: 0.5rem 1rem;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.map-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.home-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.home-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.map-content {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
  height: calc(100vh - 60px);
}

.filter-panel-container {
  width: 250px;
  background-color: #fff;
  border-right: 1px solid #ddd;
  padding: 1rem;
  overflow-y: auto;
  z-index: 5;
}

.filter-placeholder {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.map-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}
</style> 