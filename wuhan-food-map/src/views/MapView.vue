<template>
  <div class="map-view">
    <header class="map-header">
      <h1>武汉美食地图</h1>
      <div class="nav-links">
        <router-link to="/" class="home-link">返回首页</router-link>
        <router-link to="/stats" class="stats-link">查看统计</router-link>
        <router-link to="/food-culture" class="culture-link">美食文化</router-link>
      </div>
    </header>
    
    <div class="map-content">
      <div class="filter-panel-container">
        <!-- 替换占位符为实际的FilterPanel组件 -->
        <FilterPanel />
        
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
            <div class="restaurant-actions">
              <router-link :to="`/restaurant/${restaurant.id}`" class="view-detail-link">查看详情</router-link>
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
import { ref, onMounted, watch } from 'vue'
import MapContainer from '../components/MapContainer.vue'
import FilterPanel from '../components/FilterPanel.vue'
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

// 监听store中selectedRestaurant的变化
watch(() => restaurantStore.selectedRestaurant, (newSelectedRestaurant) => {
  if (newSelectedRestaurant) {
    selectedRestaurantId.value = newSelectedRestaurant.id
  } else {
    selectedRestaurantId.value = null
  }
})

onMounted(async () => {
  // 初始化获取餐厅数据
  await restaurantStore.fetchRestaurants()
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
  margin-left: 0.5rem;
}

.home-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.stats-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  margin-left: 0.5rem;
}

.stats-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.culture-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  margin-left: 0.5rem;
}

.culture-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-links {
  display: flex;
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

.restaurant-meta span:nth-child(1) {
  margin-right: 0.5rem;
}

.restaurant-actions {
  margin-top: 0.5rem;
}

.view-detail-link {
  color: #e63946;
  text-decoration: none;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.view-detail-link:hover {
  background-color: rgba(230, 57, 70, 0.1);
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