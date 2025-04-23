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
      <!-- 热力图切换按钮 -->
      <button 
        @click="toggleHeatmap" 
        class="control-btn" 
        :class="{ 'active': heatmapMode }" 
        title="切换热力图"
      >🔥</button>
      <!-- 路线规划按钮 -->
      <button 
        @click="toggleRoutePanel" 
        class="control-btn" 
        :class="{ 'active': routePanelActive }" 
        title="路线规划"
      >🗺️</button>
    </div>
    
    <!-- 路线规划面板 -->
    <RoutePanel 
      ref="routePanel"
      :isActive="routePanelActive"
      :userLocation="userLocation"
      @close="closeRoutePanel"
      @start-picking-mode="startLocationPicking"
      @route-planned="drawRoute"
      @route-cleared="clearRoute"
    />
    
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
    <!-- 地点选择提示 -->
    <div v-if="locationPickingMode" class="location-picking-hint">
      请在地图上点击选择{{ locationPickingType === 'start' ? '起点' : '终点' }}位置
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { useRestaurantStore } from '../stores/restaurant'
import RestaurantInfo from './RestaurantInfo.vue'
import BoxSelectionList from './BoxSelectionList.vue'
import RoutePanel from './RoutePanel.vue'

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

// 热力图模式状态
const heatmapMode = ref(false)

// 路线规划相关状态
const routePanelActive = ref(false)
const routePanel = ref(null)
const currentRoute = ref(null)
const routeSource = ref(null)
const locationPickingMode = ref(false)
const locationPickingType = ref(null) // 'start' 或 'end'
const userLocation = ref(null)

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
      // 初始化热力图数据
      initHeatmapSource()
      // 尝试获取用户位置
      getUserLocation()
    })
    
    mapInstance.value.on('click', (e) => {
      handleMapClick(e)
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
    // 更新热力图数据
    updateHeatmapData()
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

// 初始化热力图数据源
const initHeatmapSource = () => {
  if (!mapInstance.value) return
  
  // 添加热力图数据源
  mapInstance.value.addSource('restaurants-heat', {
    'type': 'geojson',
    'data': {
      'type': 'FeatureCollection',
      'features': []
    }
  })
  
  // 添加热力图图层
  mapInstance.value.addLayer({
    'id': 'restaurants-heat-layer',
    'type': 'heatmap',
    'source': 'restaurants-heat',
    'maxzoom': 18,
    'paint': {
      // 热力图颜色渐变
      'heatmap-color': [
        'interpolate',
        ['linear'],
        ['heatmap-density'],
        0, 'rgba(0, 0, 255, 0)',
        0.2, 'rgba(0, 255, 255, 0.5)',
        0.4, 'rgba(0, 255, 0, 0.7)',
        0.6, 'rgba(255, 255, 0, 0.8)',
        0.8, 'rgba(255, 128, 0, 0.9)',
        1, 'rgba(255, 0, 0, 1)'
      ],
      // 热力点大小
      'heatmap-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        10, 15,
        15, 25
      ],
      // 热力强度
      'heatmap-intensity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        10, 0.5,
        15, 1.5
      ],
      // 热力图权重，使用后端提供的权重属性
      'heatmap-weight': [
        'case',
        ['has', 'weight'],
        ['get', 'weight'],
        1
      ],
      // 热力图透明度
      'heatmap-opacity': 0.8
    }
  }, 'waterway-label') // 热力图在水系标签下方显示
  
  // 默认隐藏热力图
  mapInstance.value.setLayoutProperty('restaurants-heat-layer', 'visibility', 'none')
}

// 更新热力图数据
const updateHeatmapData = async () => {
  if (!mapInstance.value || !mapInstance.value.getSource('restaurants-heat')) return
  
  // 使用状态管理中的热力图数据
  if (!restaurantStore.heatmap.data) {
    // 如果没有热力图数据，则获取
    await restaurantStore.fetchHeatmapData()
  }
  
  // 如果有热力图数据，则更新地图源
  if (restaurantStore.heatmap.data) {
    mapInstance.value.getSource('restaurants-heat').setData(restaurantStore.heatmap.data)
  }
}

// 切换热力图显示
const toggleHeatmap = () => {
  if (!mapInstance.value) return
  
  // 切换热力图模式
  heatmapMode.value = !heatmapMode.value
  
  // 更新状态管理
  restaurantStore.toggleHeatmap()
  
  if (heatmapMode.value) {
    // 更新热力图数据
    updateHeatmapData()
    
    // 显示热力图图层
    mapInstance.value.setLayoutProperty('restaurants-heat-layer', 'visibility', 'visible')
    
    // 隐藏点标记（可选）
    Object.values(markers.value).forEach(marker => {
      marker.getElement().style.display = 'none'
    })
  } else {
    // 隐藏热力图图层
    mapInstance.value.setLayoutProperty('restaurants-heat-layer', 'visibility', 'none')
    
    // 显示点标记（可选）
    Object.values(markers.value).forEach(marker => {
      marker.getElement().style.display = 'block'
    })
  }
}

// 监听filteredRestaurants变化，重新渲染标记和热力图数据
watch(() => restaurantStore.filteredRestaurants, () => {
  renderRestaurants()
  updateHeatmapData()
}, { deep: true })

// 切换路线规划面板
const toggleRoutePanel = () => {
  routePanelActive.value = !routePanelActive.value
  
  // 如果关闭面板，同时清除路线
  if (!routePanelActive.value) {
    clearRoute()
  }
}

// 关闭路线规划面板
const closeRoutePanel = () => {
  routePanelActive.value = false
}

// 启动位置选择模式
const startLocationPicking = (locationType) => {
  locationPickingMode.value = true
  locationPickingType.value = locationType
  
  // 如果地图已加载，更改鼠标样式
  if (mapInstance.value) {
    mapInstance.value.getCanvas().style.cursor = 'crosshair'
  }
}

// 停止位置选择模式
const stopLocationPicking = () => {
  locationPickingMode.value = false
  locationPickingType.value = null
  
  // 恢复鼠标样式
  if (mapInstance.value) {
    mapInstance.value.getCanvas().style.cursor = ''
  }
}

// 处理地图点击事件
const handleMapClick = (e) => {
  // 如果在位置选择模式下
  if (locationPickingMode.value) {
    const coords = e.lngLat
    
    // 创建一个自定义标记作为选择的位置
    const locationId = `custom_${locationPickingType.value}_${Date.now()}`
    
    // 通知路线面板
    if (routePanel.value) {
      routePanel.value.setPickedLocation(locationPickingType.value, locationId)
    }
    
    // 在地图上添加临时标记
    addCustomLocationMarker(locationId, coords, locationPickingType.value)
    
    // 退出选择模式
    stopLocationPicking()
    
    return
  }
  
  // 原有的点击处理逻辑...
}

// 添加自定义位置标记
const addCustomLocationMarker = (id, coords, type) => {
  // 如果已存在同类型的标记，先移除它
  Object.keys(markers.value).forEach(markerId => {
    if (markerId.startsWith(`custom_${type}_`)) {
      markers.value[markerId].remove()
      delete markers.value[markerId]
    }
  })
  
  // 创建新的DOM元素
  const el = document.createElement('div')
  el.className = 'custom-location-marker'
  el.textContent = type === 'start' ? '🚩' : '🏁'
  
  // 创建标记
  const marker = new mapboxgl.Marker({
    element: el,
    draggable: false
  })
  .setLngLat(coords)
  .addTo(mapInstance.value)
  
  // 保存到标记集合
  markers.value[id] = marker
  
  // 同时保存为用户位置
  if (type === 'start') {
    userLocation.value = {
      lng: coords.lng,
      lat: coords.lat
    }
  }
}

// 绘制路线
const drawRoute = (routeData) => {
  // 保存当前路线
  currentRoute.value = routeData
  
  // 清除现有路线
  clearRoute()
  
  // 如果没有地图实例或路线数据，则返回
  if (!mapInstance.value || !routeData || !routeData.geometry) return
  
  // 检查路线源是否存在
  if (!mapInstance.value.getSource('route')) {
    // 添加路线源
    mapInstance.value.addSource('route', {
      type: 'geojson',
      data: {
        type: 'Feature',
        properties: {},
        geometry: routeData.geometry
      }
    })
    
    // 添加路线图层
    mapInstance.value.addLayer({
      id: 'route',
      type: 'line',
      source: 'route',
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#4CAF50',
        'line-width': 6,
        'line-opacity': 0.8
      }
    })
  } else {
    // 更新现有路线
    mapInstance.value.getSource('route').setData({
      type: 'Feature',
      properties: {},
      geometry: routeData.geometry
    })
  }
  
  // 添加起点和终点标记
  if (routeData.geometry && routeData.geometry.coordinates.length > 0) {
    const coordinates = routeData.geometry.coordinates
    const startCoord = coordinates[0]
    const endCoord = coordinates[coordinates.length - 1]
    
    // 添加起点和终点标记
    addCustomLocationMarker('custom_start_point', { lng: startCoord[0], lat: startCoord[1] }, 'start')
    addCustomLocationMarker('custom_end_point', { lng: endCoord[0], lat: endCoord[1] }, 'end')
    
    // 调整地图视图以适应路线
    fitMapToRoute(routeData.geometry.coordinates)
  }
}

// 清除路线
const clearRoute = () => {
  // 清除当前路线数据
  currentRoute.value = null
  
  // 移除地图上的路线图层和源
  if (mapInstance.value) {
    if (mapInstance.value.getLayer('route')) {
      mapInstance.value.removeLayer('route')
    }
    
    if (mapInstance.value.getSource('route')) {
      mapInstance.value.removeSource('route')
    }
    
    // 移除标记
    Object.keys(markers.value).forEach(markerId => {
      if (markerId.startsWith('custom_')) {
        markers.value[markerId].remove()
        delete markers.value[markerId]
      }
    })
  }
}

// 调整地图视图以适应路线
const fitMapToRoute = (coordinates) => {
  if (!mapInstance.value || !coordinates || coordinates.length === 0) return
  
  // 创建包含所有坐标的边界框
  const bounds = coordinates.reduce((bounds, coord) => {
    return bounds.extend(coord)
  }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]))
  
  // 调整地图视图
  mapInstance.value.fitBounds(bounds, {
    padding: 50,
    maxZoom: 15
  })
}

// 获取用户位置
const getUserLocation = () => {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
        
        // 可选：在地图上添加用户位置标记
        if (mapInstance.value) {
          addCustomLocationMarker('user_current_location', userLocation.value, 'user')
        }
      },
      (error) => {
        console.error('无法获取用户位置:', error)
      }
    )
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

/* 添加路线规划相关样式 */
.custom-location-marker {
  font-size: 24px;
  cursor: pointer;
}

.location-picking-hint {
  position: absolute;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  z-index: 10;
}
</style> 