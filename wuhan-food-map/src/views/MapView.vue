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
        
        <div v-if="restaurantStore.loading" class="loading-indicator">
          <span>加载中...</span>
        </div>
        <div v-else-if="restaurantStore.error" class="error-message">
          <span>{{ restaurantStore.error }}</span>
        </div>
        <div v-else class="restaurant-list">
          <h3>餐厅列表</h3>
          <div 
            v-for="restaurant in restaurantStore.filteredRestaurants" 
            :key="restaurant.id"
            class="restaurant-item"
            :class="{ 'active': selectedRestaurantId === restaurant.id }"
            @click="selectRestaurant(restaurant)"
          >
            <div class="restaurant-name">{{ restaurant.name }}</div>
            <div class="restaurant-meta">
              <span>{{ restaurant.food_type || '未分类' }}</span>
              <span>{{ restaurant.district || '未知区域' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="map-wrapper">
        <MapContainer 
          :initial-center="[114.3008, 30.5433]" 
          :initial-zoom="12"
          @map-loaded="handleMapLoaded"
          @map-click="handleMapClick"
          @marker-click="handleMarkerClick"
          ref="mapContainerRef"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MapContainer from '../components/MapContainer.vue'
import { useRestaurantStore } from '../stores/restaurant'

// 餐厅状态管理
const restaurantStore = useRestaurantStore()

// 地图实例引用
const mapContainerRef = ref(null)
const mapInstance = ref(null)

// 选中的餐厅ID
const selectedRestaurantId = ref(null)

// 地图加载完成处理
const handleMapLoaded = (map) => {
  console.log('地图在MapView中加载完成')
  mapInstance.value = map
}

// 地图点击事件处理
const handleMapClick = (e) => {
  console.log('地图点击坐标:', e.lngLat)
}

// 标记点击事件处理
const handleMarkerClick = (restaurant) => {
  console.log('餐厅标记点击:', restaurant.name)
  selectedRestaurantId.value = restaurant.id
}

// 从列表选择餐厅
const selectRestaurant = (restaurant) => {
  selectedRestaurantId.value = restaurant.id
  
  // 触发地图组件中的标记点击
  if (mapContainerRef.value) {
    mapContainerRef.value.handleMarkerClick(restaurant)
  }
}

onMounted(async () => {
  // 可以在此处初始化数据，但现在已经在MapContainer中处理
})
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
  width: 300px;
  background-color: #fff;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  z-index: 5;
}

.filter-placeholder {
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.restaurant-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 1rem;
}

.restaurant-list h3 {
  margin: 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
  color: #333;
}

.restaurant-item {
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.2s ease;
}

.restaurant-item:hover {
  background-color: #f5f5f5;
  border-left-color: #e63946;
}

.restaurant-item.active {
  background-color: #f8f9fa;
  border-left-color: #e63946;
}

.restaurant-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.restaurant-meta {
  display: flex;
  font-size: 0.8rem;
  color: #666;
}

.restaurant-meta span {
  margin-right: 0.5rem;
}

.loading-indicator, .error-message {
  padding: 1rem;
  text-align: center;
  color: #666;
}

.error-message {
  color: #e63946;
}

.map-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
}
</style> 