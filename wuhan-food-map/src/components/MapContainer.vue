<template>
  <div class="map-container">
    <div id="map" ref="mapElement" class="map-element"></div>
    <div class="map-controls">
      <button @click="zoomIn" class="control-btn" title="放大">+</button>
      <button @click="zoomOut" class="control-btn" title="缩小">-</button>
      <button @click="resetView" class="control-btn" title="重置视图">⟳</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// 定义props
const props = defineProps({
  // 初始中心点，默认为武汉市中心坐标
  initialCenter: {
    type: Array,
    default: () => [114.3008, 30.5433]
  },
  // 初始缩放级别
  initialZoom: {
    type: Number,
    default: 12
  },
  // 地图样式
  mapStyle: {
    type: String,
    default: 'mapbox://styles/mapbox/streets-v11'
  }
})

// 定义事件
const emit = defineEmits(['map-loaded', 'map-click', 'map-move'])

// 引用DOM元素
const mapElement = ref(null)

// 地图实例
const mapInstance = ref(null)

// 初始化地图
const initMap = () => {
  // 设置Token（真实项目中应从环境变量获取）
  mapboxgl.accessToken = 'pk.eyJ1IjoiemhlbmdqaWFtaW5nIiwiYSI6ImNtOXM1ZTViaTA0dTIyanI1OHVjMDZrOW8ifQ.awqJ-KNyvXXq4drMK7HqWw'
  
  try {
    // 创建地图
    mapInstance.value = new mapboxgl.Map({
      container: mapElement.value,
      style: props.mapStyle,
      center: props.initialCenter,
      zoom: props.initialZoom,
      attributionControl: true
    })
    
    // 添加导航控件
    mapInstance.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
    
    // 添加比例尺
    mapInstance.value.addControl(new mapboxgl.ScaleControl({
      maxWidth: 100,
      unit: 'metric'
    }), 'bottom-left')
    
    // 添加全屏控件
    mapInstance.value.addControl(new mapboxgl.FullscreenControl(), 'top-right')
    
    // 地图事件监听
    mapInstance.value.on('load', () => {
      console.log('地图加载完成')
      emit('map-loaded', mapInstance.value)
    })
    
    mapInstance.value.on('click', (e) => {
      emit('map-click', e)
    })
    
    mapInstance.value.on('moveend', () => {
      const center = mapInstance.value.getCenter()
      const zoom = mapInstance.value.getZoom()
      emit('map-move', { center, zoom })
    })
  } catch (error) {
    console.error('地图初始化失败:', error)
  }
}

// 暴露方法给父组件
const getMapInstance = () => mapInstance.value
defineExpose({ getMapInstance })

// 地图控制方法
const zoomIn = () => {
  if (mapInstance.value) {
    mapInstance.value.zoomIn()
  }
}

const zoomOut = () => {
  if (mapInstance.value) {
    mapInstance.value.zoomOut()
  }
}

const resetView = () => {
  if (mapInstance.value) {
    mapInstance.value.flyTo({
      center: props.initialCenter,
      zoom: props.initialZoom,
      essential: true,
      duration: 1000
    })
  }
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
  overflow: hidden;
}

.map-element {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.map-controls {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1;
}

.control-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #4369b2;
  border: none;
  color: white;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: all 0.2s ease;
}

.control-btn:hover {
  background-color: #3a5a9b;
  transform: scale(1.05);
}

.control-btn:active {
  transform: scale(0.95);
}
</style> 