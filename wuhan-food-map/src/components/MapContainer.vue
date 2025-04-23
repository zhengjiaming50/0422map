<template>
  <div class="map-container">
    <div id="map" ref="mapElement" class="map-element"></div>
    <div class="map-controls">
      <button @click="zoomIn" class="control-btn" title="放大">+</button>
      <button @click="zoomOut" class="control-btn" title="缩小">-</button>
      <button @click="resetView" class="control-btn" title="重置视图">⟳</button>
      <button 
        @click="toggleBoxSelection" 
        class="control-btn" 
        :class="{ 'active': boxSelectionMode }" 
        title="框选区域"
      >◰</button>
      <button 
        @click="toggleHeatmap" 
        class="control-btn" 
        :class="{ 'active': heatmapVisible }" 
        title="热力图"
      >🔥</button>
    </div>
    <div v-if="selectedRestaurant" class="restaurant-detail-panel">
      <RestaurantInfo 
        :restaurant="selectedRestaurant" 
        @close="closeRestaurantInfo" 
      />
    </div>
    <div class="box-selection-panel">
      <BoxSelectionList 
        @close="closeBoxSelection"
        @select-restaurant="handleMarkerClick"
      />
    </div>
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
    <!-- 框选操作提示 -->
    <div v-if="boxSelectionMode" class="box-selection-hint">
      请在地图上拖动鼠标框选区域
    </div>
    <!-- 热力图图例 -->
    <div v-if="heatmapVisible" class="heatmap-legend">
      <div class="legend-title">餐厅密度</div>
      <div class="legend-gradient"></div>
      <div class="legend-labels">
        <span>低</span>
        <span>高</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { useRestaurantStore } from '../stores/restaurant'
import RestaurantInfo from './RestaurantInfo.vue'
import BoxSelectionList from './BoxSelectionList.vue'

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

// 框选模式状态
const boxSelectionMode = ref(false)

// 框选起始点
const boxStart = ref(null)

// 框选矩形实例
const boxElement = ref(null)

// 热力图状态
const heatmapVisible = computed(() => restaurantStore.heatmap.visible)

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
      // 初始化框选相关事件
      initBoxSelectionEvents()
      // 初始化热力图
      initHeatmapLayer()
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

// 初始化框选事件
const initBoxSelectionEvents = () => {
  if (!mapInstance.value) return
  
  // 鼠标按下事件
  mapInstance.value.on('mousedown', (e) => {
    if (!boxSelectionMode.value) return
    
    // 阻止默认行为和事件冒泡
    e.preventDefault()
    
    // 记录起始点
    boxStart.value = e.point
    
    // 创建框选矩形
    createBoxElement()
    
    // 添加鼠标移动和松开事件
    mapInstance.value.on('mousemove', onMouseMove)
    mapInstance.value.once('mouseup', onMouseUp)
  })
}

// 创建框选矩形元素
const createBoxElement = () => {
  // 移除可能存在的旧元素
  if (boxElement.value) {
    boxElement.value.remove()
  }
  
  // 创建新元素
  boxElement.value = document.createElement('div')
  boxElement.value.className = 'box-selection-rect'
  mapElement.value.appendChild(boxElement.value)
}

// 鼠标移动时更新框选矩形
const onMouseMove = (e) => {
  if (!boxStart.value || !boxElement.value) return
  
  // 计算矩形坐标
  const minX = Math.min(boxStart.value.x, e.point.x)
  const maxX = Math.max(boxStart.value.x, e.point.x)
  const minY = Math.min(boxStart.value.y, e.point.y)
  const maxY = Math.max(boxStart.value.y, e.point.y)
  
  // 设置矩形样式
  boxElement.value.style.left = `${minX}px`
  boxElement.value.style.top = `${minY}px`
  boxElement.value.style.width = `${maxX - minX}px`
  boxElement.value.style.height = `${maxY - minY}px`
}

// 鼠标松开时完成框选
const onMouseUp = (e) => {
  if (!boxStart.value) return
  
  // 移除监听器
  mapInstance.value.off('mousemove', onMouseMove)
  
  // 计算边界框地理坐标
  const sw = mapInstance.value.unproject([
    Math.min(boxStart.value.x, e.point.x),
    Math.max(boxStart.value.y, e.point.y)
  ])
  
  const ne = mapInstance.value.unproject([
    Math.max(boxStart.value.x, e.point.x),
    Math.min(boxStart.value.y, e.point.y)
  ])
  
  // 查询边界框内的餐厅
  fetchRestaurantsInBox({
    minLng: sw.lng,
    minLat: sw.lat,
    maxLng: ne.lng,
    maxLat: ne.lat
  })
  
  // 重置框选状态
  boxStart.value = null
  
  // 显示边界框
  displayBoxBounds(sw, ne)
}

// 显示框选边界
const displayBoxBounds = (sw, ne) => {
  if (!mapInstance.value) return
  
  // 如果已有边界图层，先移除
  if (mapInstance.value.getSource('box-bounds')) {
    mapInstance.value.removeLayer('box-fill')
    mapInstance.value.removeLayer('box-outline')
    mapInstance.value.removeSource('box-bounds')
  }
  
  // 添加边界数据源
  mapInstance.value.addSource('box-bounds', {
    'type': 'geojson',
    'data': {
      'type': 'Feature',
      'geometry': {
        'type': 'Polygon',
        'coordinates': [[
          [sw.lng, sw.lat],
          [ne.lng, sw.lat],
          [ne.lng, ne.lat],
          [sw.lng, ne.lat],
          [sw.lng, sw.lat]
        ]]
      }
    }
  })
  
  // 添加填充图层
  mapInstance.value.addLayer({
    'id': 'box-fill',
    'type': 'fill',
    'source': 'box-bounds',
    'layout': {},
    'paint': {
      'fill-color': '#4369b2',
      'fill-opacity': 0.15
    }
  })
  
  // 添加边框图层
  mapInstance.value.addLayer({
    'id': 'box-outline',
    'type': 'line',
    'source': 'box-bounds',
    'layout': {},
    'paint': {
      'line-color': '#4369b2',
      'line-width': 2
    }
  })
  
  // 移除临时矩形
  if (boxElement.value) {
    boxElement.value.remove()
    boxElement.value = null
  }
}

// 查询边界框内的餐厅
const fetchRestaurantsInBox = async (bounds) => {
  loading.value = true
  
  try {
    await restaurantStore.fetchRestaurantsInBox(bounds)
    
    // 切换到框选模式
    boxSelectionMode.value = true
  } catch (error) {
    console.error('获取边界框内餐厅失败:', error)
  } finally {
    loading.value = false
  }
}

// 初始化热力图图层
const initHeatmapLayer = () => {
  if (!mapInstance.value) return
  
  // 等待地图样式加载完成
  mapInstance.value.on('style.load', () => {
    // 如果已有热力图数据源，先移除
    if (mapInstance.value.getSource('restaurants-heat')) {
      mapInstance.value.removeLayer('restaurants-heat')
      mapInstance.value.removeSource('restaurants-heat')
    }
    
    // 创建热力图数据源
    mapInstance.value.addSource('restaurants-heat', {
      'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': []
      }
    })
    
    // 创建热力图图层
    mapInstance.value.addLayer({
      'id': 'restaurants-heat',
      'type': 'heatmap',
      'source': 'restaurants-heat',
      'layout': {
        'visibility': 'none'
      },
      'paint': {
        // 热力图权重，基于point_count属性
        'heatmap-weight': [
          'interpolate',
          ['linear'],
          ['get', 'weight'],
          0, 0,
          10, 1
        ],
        // 热力图强度
        'heatmap-intensity': [
          'interpolate',
          ['linear'],
          ['zoom'],
          8, 0.5,
          16, 1.5
        ],
        // 色彩渐变
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(0, 0, 255, 0)',
          0.2, 'rgba(0, 255, 255, 0.6)',
          0.4, 'rgba(0, 255, 0, 0.6)',
          0.6, 'rgba(255, 255, 0, 0.6)',
          0.8, 'rgba(255, 128, 0, 0.7)',
          1, 'rgba(255, 0, 0, 0.8)'
        ],
        // 热点半径
        'heatmap-radius': [
          'interpolate',
          ['linear'],
          ['zoom'],
          8, 10,
          16, 40
        ],
        // 不透明度
        'heatmap-opacity': 0.8
      }
    })
  })
}

// 更新热力图数据
const updateHeatmapData = () => {
  if (!mapInstance.value || !mapInstance.value.getSource('restaurants-heat')) return
  
  const restaurants = restaurantStore.heatmap.data
  
  // 转换为GeoJSON格式
  const geojson = {
    type: 'FeatureCollection',
    features: restaurants.map(restaurant => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [restaurant.longitude, restaurant.latitude]
      },
      properties: {
        id: restaurant.id,
        weight: restaurant.weight || 1
      }
    }))
  }
  
  // 更新数据源
  mapInstance.value.getSource('restaurants-heat').setData(geojson)
}

// 切换热力图显示状态
const toggleHeatmap = async () => {
  // 调用状态管理的toggleHeatmap方法
  await restaurantStore.toggleHeatmap()
  
  if (!mapInstance.value || !mapInstance.value.getLayer('restaurants-heat')) return

  if (restaurantStore.heatmap.visible) {
    // 更新热力图数据
    updateHeatmapData()
    
    // 显示热力图层
    mapInstance.value.setLayoutProperty('restaurants-heat', 'visibility', 'visible')
    
    // 隐藏标记
    Object.values(markers.value).forEach(marker => {
      marker.getElement().style.display = 'none'
    })
  } else {
    // 隐藏热力图层
    mapInstance.value.setLayoutProperty('restaurants-heat', 'visibility', 'none')
    
    // 显示标记
    Object.values(markers.value).forEach(marker => {
      marker.getElement().style.display = 'flex'
    })
  }
}

// 切换框选模式
const toggleBoxSelection = () => {
  // 切换框选模式
  boxSelectionMode.value = !boxSelectionMode.value
  
  if (!boxSelectionMode.value) {
    // 如果关闭框选模式，清除框选结果
    clearBoxSelection()
  } else {
    // 激活框选模式，光标变为十字形
    mapElement.value.style.cursor = 'crosshair'
  }
}

// 清除框选
const clearBoxSelection = () => {
  if (!mapInstance.value) return
  
  // 重置光标
  mapElement.value.style.cursor = ''
  
  // 移除边界显示
  if (mapInstance.value.getSource('box-bounds')) {
    mapInstance.value.removeLayer('box-fill')
    mapInstance.value.removeLayer('box-outline')
    mapInstance.value.removeSource('box-bounds')
  }
  
  // 清除框选矩形
  if (boxElement.value) {
    boxElement.value.remove()
    boxElement.value = null
  }
  
  // 重置框选状态
  boxStart.value = null
  
  // 清除状态管理里的框选结果
  restaurantStore.clearBoxSelection()
}

// 关闭框选面板
const closeBoxSelection = () => {
  // 关闭框选模式
  boxSelectionMode.value = false
  
  // 清除框选
  clearBoxSelection()
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
  
  // 根据餐厅类型选择不同图标
  let icon = '🍜';
  if (restaurant.food_type) {
    const foodType = restaurant.food_type.toLowerCase();
    if (foodType.includes('火锅')) icon = '🍲';
    else if (foodType.includes('烧烤')) icon = '🍢';
    else if (foodType.includes('西餐')) icon = '🍔';
    else if (foodType.includes('粤菜')) icon = '🥘';
    else if (foodType.includes('小吃')) icon = '🥟';
    else if (foodType.includes('甜点')) icon = '🍰';
    else if (foodType.includes('咖啡')) icon = '☕';
    else if (foodType.includes('茶')) icon = '🍵';
  }
  
  markerElement.innerHTML = icon
  
  // 如果热力图显示中，则隐藏标记
  if (restaurantStore.heatmap.visible) {
    markerElement.style.display = 'none'
  }
  
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
  // 更新选中的餐厅
  selectedRestaurant.value = restaurant
  
  // 获取餐厅详情
  restaurantStore.setSelectedRestaurant(restaurant)
  
  // 高亮显示选中的标记
  highlightSelectedMarker(restaurant.id)
  
  // 缩放到餐厅位置
  mapInstance.value.flyTo({
    center: [restaurant.longitude, restaurant.latitude],
    zoom: 16, // 放大级别更高，能更清楚看到餐厅位置
    essential: true,
    duration: 1000
  })
  
  emit('marker-click', restaurant)
}

// 高亮显示选中的标记
const highlightSelectedMarker = (selectedId) => {
  // 移除所有标记的高亮样式
  Object.keys(markers.value).forEach(id => {
    const marker = markers.value[id];
    const element = marker.getElement();
    element.classList.remove('selected');
  });
  
  // 添加高亮样式到选中的标记
  if (markers.value[selectedId]) {
    const element = markers.value[selectedId].getElement();
    element.classList.add('selected');
  }
}

// 关闭餐厅详情
const closeRestaurantInfo = () => {
  selectedRestaurant.value = null
  restaurantStore.clearSelectedRestaurant()
  
  // 移除所有标记的高亮样式
  Object.keys(markers.value).forEach(id => {
    const marker = markers.value[id];
    const element = marker.getElement();
    element.classList.remove('selected');
  });
}

// 暴露方法给父组件
const getMapInstance = () => mapInstance.value
defineExpose({ getMapInstance, handleMarkerClick })

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
    restaurantStore.clearSelectedRestaurant()
    
    // 移除所有标记的高亮样式
    Object.keys(markers.value).forEach(id => {
      const marker = markers.value[id];
      const element = marker.getElement();
      element.classList.remove('selected');
    });
  }
}

// 监听filteredRestaurants变化，重新渲染标记
watch(() => restaurantStore.filteredRestaurants, () => {
  renderRestaurants()
}, { deep: true })

// 监听热力图数据变化，更新热力图
watch(() => restaurantStore.heatmap.data, () => {
  if (restaurantStore.heatmap.visible) {
    updateHeatmapData()
  }
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

.control-btn.active {
  background-color: #e63946;
}

.restaurant-detail-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 2;
}

.box-selection-panel {
  position: absolute;
  top: 20px;
  right: 20px;
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

/* 餐厅标记样式 */
:deep(.restaurant-marker) {
  width: 30px;
  height: 30px;
  background-color: #e63946;
  border-radius: 50%;
  color: white;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

:deep(.restaurant-marker:hover) {
  transform: scale(1.1);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
}

:deep(.restaurant-marker.selected) {
  background-color: #457b9d;
  transform: scale(1.2);
  box-shadow: 0 0 0 3px rgba(69, 123, 157, 0.5), 0 3px 6px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

/* 框选矩形样式 */
.box-selection-rect {
  position: absolute;
  background-color: rgba(67, 105, 178, 0.2);
  border: 2px solid #4369b2;
  pointer-events: none;
  z-index: 2;
}

.box-selection-hint {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  z-index: 3;
}

/* 热力图图例样式 */
.heatmap-legend {
  position: absolute;
  bottom: 30px;
  right: 20px;
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  z-index: 2;
}

.legend-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
  text-align: center;
}

.legend-gradient {
  width: 150px;
  height: 15px;
  margin: 5px 0;
  background: linear-gradient(to right, 
    rgba(0, 0, 255, 0.6) 0%, 
    rgba(0, 255, 255, 0.6) 20%, 
    rgba(0, 255, 0, 0.6) 40%, 
    rgba(255, 255, 0, 0.6) 60%, 
    rgba(255, 128, 0, 0.7) 80%, 
    rgba(255, 0, 0, 0.8) 100%
  );
  border-radius: 3px;
}

.legend-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #555;
}
</style> 