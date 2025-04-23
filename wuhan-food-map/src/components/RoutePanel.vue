<template>
  <div class="route-panel" :class="{ 'active': isActive }">
    <div class="route-panel-header">
      <h3>路线规划</h3>
      <button class="close-btn" @click="close">×</button>
    </div>
    
    <div class="route-form">
      <div class="form-group">
        <label>起点</label>
        <div class="location-input">
          <select v-model="startPoint" class="location-select">
            <option value="">请选择起点</option>
            <option value="user_location" v-if="userLocation">当前位置</option>
            <option v-for="restaurant in restaurants" :key="`start-${restaurant.id}`" :value="restaurant.id">
              {{ restaurant.name }}
            </option>
          </select>
          <button class="map-pick-btn" @click="startPickingMode('start')" title="在地图上选择">📍</button>
        </div>
      </div>
      
      <div class="form-group">
        <label>终点</label>
        <div class="location-input">
          <select v-model="endPoint" class="location-select">
            <option value="">请选择终点</option>
            <option value="user_location" v-if="userLocation">当前位置</option>
            <option v-for="restaurant in restaurants" :key="`end-${restaurant.id}`" :value="restaurant.id">
              {{ restaurant.name }}
            </option>
          </select>
          <button class="map-pick-btn" @click="startPickingMode('end')" title="在地图上选择">📍</button>
        </div>
      </div>
      
      <div class="travel-mode">
        <label>出行方式</label>
        <div class="travel-mode-options">
          <button 
            class="travel-mode-btn" 
            :class="{ 'active': travelMode === 'walking' }"
            @click="travelMode = 'walking'"
            title="步行"
          >
            🚶
          </button>
          <button 
            class="travel-mode-btn" 
            :class="{ 'active': travelMode === 'driving' }"
            @click="travelMode = 'driving'"
            title="驾车"
          >
            🚗
          </button>
          <button 
            class="travel-mode-btn" 
            :class="{ 'active': travelMode === 'transit' }"
            @click="travelMode = 'transit'"
            title="公交"
          >
            🚌
          </button>
        </div>
      </div>
      
      <button 
        class="plan-btn" 
        @click="planRoute" 
        :disabled="!isFormValid || isLoading"
      >
        {{ isLoading ? '规划中...' : '开始规划' }}
      </button>
    </div>
    
    <div v-if="route" class="route-result">
      <div class="route-summary">
        <div class="route-info">
          <div class="route-distance">
            <span>总距离:</span> {{ formatDistance(route.distance) }}
          </div>
          <div class="route-duration">
            <span>预计时间:</span> {{ formatDuration(route.duration) }}
          </div>
        </div>
      </div>
      
      <div class="route-steps">
        <h4>导航指引</h4>
        <ul class="steps-list">
          <li v-for="(step, index) in route.steps" :key="index" class="step-item">
            <div class="step-icon">{{ getStepIcon(step.maneuver) }}</div>
            <div class="step-instruction">{{ step.instruction }}</div>
            <div class="step-distance">{{ formatDistance(step.distance) }}</div>
          </li>
        </ul>
      </div>
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'
import { routeApi } from '../services/api'

// 定义props
const props = defineProps({
  isActive: {
    type: Boolean,
    default: false
  },
  userLocation: {
    type: Object,
    default: null
  }
})

// 定义事件
const emit = defineEmits([
  'close', 
  'start-picking-mode', 
  'route-planned', 
  'route-cleared'
])

// 餐厅状态管理
const restaurantStore = useRestaurantStore()
const restaurants = computed(() => restaurantStore.restaurants)

// 起点和终点
const startPoint = ref('')
const endPoint = ref('')
const travelMode = ref('walking')
const isPickingLocation = ref(false)
const pickingFor = ref(null) // 'start' or 'end'

// 用于存储自定义位置坐标的映射
const customLocations = ref({})

// 路线信息
const route = ref(null)
const error = ref(null)
const isLoading = ref(false)

// 表单验证
const isFormValid = computed(() => {
  return startPoint.value && endPoint.value && startPoint.value !== endPoint.value
})

// 关闭面板
const close = () => {
  emit('close')
  clearRoute()
}

// 清除路线
const clearRoute = () => {
  route.value = null
  error.value = null
  emit('route-cleared')
}

// 开始地图选点模式
const startPickingMode = (pointType) => {
  pickingFor.value = pointType
  emit('start-picking-mode', pointType)
}

// 设置位置选择结果
const setPickedLocation = (pointType, locationId) => {
  if (pointType === 'start') {
    startPoint.value = locationId
  } else if (pointType === 'end') {
    endPoint.value = locationId
  }
}

// 存储自定义位置坐标
const setCustomLocationCoordinates = (locationId, coordinates) => {
  customLocations.value[locationId] = coordinates
}

// 规划路线
const planRoute = async () => {
  if (!isFormValid.value) return
  
  try {
    isLoading.value = true
    error.value = null
    
    // 获取起点和终点信息
    const start = await getLocationCoordinates(startPoint.value)
    const end = await getLocationCoordinates(endPoint.value)
    
    if (!start || !end) {
      error.value = '无法获取起点或终点坐标'
      return
    }
    
    // 调用路线规划服务
    const routeData = await routeApi.getRoute({
      start,
      end,
      mode: travelMode.value
    })
    
    route.value = routeData
    emit('route-planned', routeData)
  } catch (err) {
    error.value = `规划路线失败: ${err.message}`
    console.error('规划路线错误:', err)
  } finally {
    isLoading.value = false
  }
}

// 获取位置坐标
const getLocationCoordinates = async (locationId) => {
  if (!locationId) return null
  
  // 如果是当前位置
  if (locationId === 'user_location') {
    return props.userLocation ? 
      { lng: props.userLocation.lng, lat: props.userLocation.lat } : 
      null
  }
  
  // 处理自定义位置（在地图上选择的位置）
  if (locationId.startsWith('custom_')) {
    // 如果在customLocations中有该位置的坐标，则使用它
    if (customLocations.value[locationId]) {
      return customLocations.value[locationId]
    }
    
    // 尝试从DOM中获取标记位置
    const marker = document.querySelector(`.custom-location-marker[data-id="${locationId}"]`)
    if (marker && marker.dataset.lat && marker.dataset.lng) {
      return { 
        lng: parseFloat(marker.dataset.lng), 
        lat: parseFloat(marker.dataset.lat)
      }
    }
    
    console.error('无法获取自定义位置坐标:', locationId)
    return null
  }
  
  // 如果是餐厅
  const restaurant = restaurants.value.find(r => r.id == locationId)
  if (restaurant) {
    return { lng: restaurant.longitude, lat: restaurant.latitude }
  }
  
  return null
}

// 格式化距离
const formatDistance = (meters) => {
  if (meters < 1000) {
    return `${Math.round(meters)} 米`
  } else {
    return `${(meters/1000).toFixed(1)} 公里`
  }
}

// 格式化时间
const formatDuration = (seconds) => {
  if (seconds < 60) {
    return `${Math.round(seconds)} 秒`
  } else if (seconds < 3600) {
    return `${Math.floor(seconds/60)} 分钟`
  } else {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours} 小时 ${minutes} 分钟`
  }
}

// 获取步骤图标
const getStepIcon = (maneuver) => {
  const icons = {
    'turn-left': '↰',
    'turn-right': '↱',
    'straight': '↑',
    'merge': '↣',
    'fork': '⑂',
    'roundabout': '⟳',
    'exit': '↲',
    'arrive': '🏁',
    'depart': '🚩'
  }
  
  return icons[maneuver] || '↝'
}

// 对外暴露方法
defineExpose({
  setPickedLocation,
  setCustomLocationCoordinates,
  clearRoute
})
</script>

<style scoped>
.route-panel {
  width: 320px;
  max-height: 80vh;
  overflow-y: auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 16px;
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
  display: none;
}

.route-panel.active {
  display: block;
}

.route-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.route-panel-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: #555;
}

.location-input {
  display: flex;
  gap: 8px;
}

.location-select {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.map-pick-btn {
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
}

.map-pick-btn:hover {
  background: #e5e5e5;
}

.travel-mode {
  margin-bottom: 16px;
}

.travel-mode-options {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.travel-mode-btn {
  flex: 1;
  padding: 8px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.travel-mode-btn.active {
  background: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.plan-btn {
  width: 100%;
  padding: 10px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
}

.plan-btn:hover:not(:disabled) {
  background: #3d9440;
}

.plan-btn:disabled {
  background: #a5d6a7;
  cursor: not-allowed;
}

.route-result {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 16px;
}

.route-summary {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.route-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.route-distance, .route-duration {
  font-size: 14px;
}

.route-distance span, .route-duration span {
  font-weight: 500;
  color: #555;
}

.route-steps h4 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 16px;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.step-item {
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
  align-items: center;
}

.step-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 12px;
}

.step-instruction {
  flex: 1;
  font-size: 14px;
}

.step-distance {
  font-size: 12px;
  color: #888;
  margin-left: 8px;
}

.error-message {
  margin-top: 16px;
  padding: 12px;
  background: #ffebee;
  color: #c62828;
  border-radius: 4px;
  font-size: 14px;
}
</style> 