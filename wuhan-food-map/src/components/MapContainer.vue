<template>
  <div class="map-container">
    <div id="map" ref="mapElement" class="map-element"></div>
    <div class="map-controls">
      <button @click="zoomIn" class="control-btn">+</button>
      <button @click="zoomOut" class="control-btn">-</button>
      <button @click="resetView" class="control-btn">⟳</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// 地图配置
const mapConfig = {
  initialCenter: [114.3008, 30.5433], // 武汉市中心坐标
  initialZoom: 12,
  style: 'mapbox://styles/mapbox/streets-v11',
  token: 'pk.eyJ1IjoiZXhhbXBsZXVzZXIiLCJhIjoiY2xoajN2aGNuMDJpYjNkbXV1ZHB6aGxjYyJ9.example' // 临时token
}

// 引用DOM元素
const mapElement = ref(null)

// 地图实例
const mapInstance = ref(null)

// 初始化地图
const initMap = () => {
  // 设置Token
  mapboxgl.accessToken = mapConfig.token
  
  // 创建地图
  mapInstance.value = new mapboxgl.Map({
    container: mapElement.value,
    style: mapConfig.style,
    center: mapConfig.initialCenter,
    zoom: mapConfig.initialZoom
  })
  
  // 添加导航控件
  mapInstance.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
  
  // 地图加载完成事件
  mapInstance.value.on('load', () => {
    console.log('地图加载完成')
  })
}

// 地图控制方法
const zoomIn = () => {
  mapInstance.value.zoomIn()
}

const zoomOut = () => {
  mapInstance.value.zoomOut()
}

const resetView = () => {
  mapInstance.value.flyTo({
    center: mapConfig.initialCenter,
    zoom: mapConfig.initialZoom,
    essential: true
  })
}

// 生命周期钩子
onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (mapInstance.value) {
    mapInstance.value.remove()
  }
})
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.map-element {
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
  z-index: 1;
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