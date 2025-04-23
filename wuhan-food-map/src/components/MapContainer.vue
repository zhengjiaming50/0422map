<template>
  <div class="map-container">
    <div id="map" ref="mapElement" class="map-element"></div>
    <div class="map-controls">
      <button @click="zoomIn" class="control-btn" title="放大">+</button>
      <button @click="zoomOut" class="control-btn" title="缩小">-</button>
      <button @click="resetView" class="control-btn" title="重置视图">⟳</button>
    </div>
    <div v-if="selectedRestaurant" class="restaurant-detail-panel">
      <RestaurantInfo 
        :restaurant="selectedRestaurant" 
        @close="closeRestaurantInfo" 
      />
    </div>
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { useRestaurantStore } from '../stores/restaurant'
import RestaurantInfo from './RestaurantInfo.vue'

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
  },
  // 餐厅列表
  restaurants: {
    type: Array,
    default: () => []
  }
})

// 定义事件
const emit = defineEmits(['map-loaded', 'map-click', 'map-move', 'marker-click'])

// 引用DOM元素
const mapElement = ref(null)

// 地图实例
const mapInstance = ref(null)

// 餐厅标记集合
const markers = ref({})

// 餐厅状态管理
const restaurantStore = useRestaurantStore()

// 选中的餐厅
const selectedRestaurant = ref(null)

// 加载状态
const loading = ref(false)

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
      fetchRestaurants()
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

// 获取餐厅数据
const fetchRestaurants = async () => {
  loading.value = true
  try {
    await restaurantStore.fetchRestaurants()
    renderRestaurants()
  } catch (error) {
    console.error('获取餐厅数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 渲染餐厅标记
const renderRestaurants = () => {
  // 清除现有标记
  clearMarkers()
  
  // 为每个餐厅创建标记
  restaurantStore.filteredRestaurants.forEach(restaurant => {
    addMarker(restaurant)
  })
}

// 添加单个餐厅标记
const addMarker = (restaurant) => {
  if (!mapInstance.value || !restaurant.latitude || !restaurant.longitude) return
  
  // 创建标记元素
  const markerElement = document.createElement('div')
  markerElement.className = 'restaurant-marker'
  markerElement.innerHTML = '🍜'
  
  // 创建Mapbox标记
  const marker = new mapboxgl.Marker(markerElement)
    .setLngLat([restaurant.longitude, restaurant.latitude])
    .addTo(mapInstance.value)
  
  // 标记点击事件
  markerElement.addEventListener('click', () => {
    handleMarkerClick(restaurant)
  })
  
  // 存储标记引用
  markers.value[restaurant.id] = marker
}

// 清除所有标记
const clearMarkers = () => {
  Object.values(markers.value).forEach(marker => {
    marker.remove()
  })
  markers.value = {}
}

// 标记点击处理
const handleMarkerClick = (restaurant) => {
  selectedRestaurant.value = restaurant
  
  // 缩放到餐厅位置
  mapInstance.value.flyTo({
    center: [restaurant.longitude, restaurant.latitude],
    zoom: 15,
    essential: true,
    duration: 1000
  })
  
  emit('marker-click', restaurant)
}

// 关闭餐厅详情
const closeRestaurantInfo = () => {
  selectedRestaurant.value = null
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
    
    // 关闭详情面板并清除选中状态
    selectedRestaurant.value = null
  }
}

// 监听filteredRestaurants变化，重新渲染标记
watch(() => restaurantStore.filteredRestaurants, () => {
  renderRestaurants()
}, { deep: true })

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

.restaurant-detail-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 2;
}

.restaurant-marker {
  background-color: #e63946;
  color: white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
  cursor: pointer;
  transition: all 0.2s ease;
}

.restaurant-marker:hover {
  transform: scale(1.1);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 