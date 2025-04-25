<template>
  <div class="map-view">
    <header class="map-header cyber-header">
      <h1 class="neon-text">武汉美食地图</h1>
      <div class="nav-links">
        <router-link to="/" class="cyber-link">返回首页</router-link>
        <router-link to="/stats" class="cyber-link">查看统计</router-link>
        <router-link to="/food-culture" class="cyber-link">美食文化</router-link>
      </div>
    </header>
    
    <div class="map-content">
      <div class="filter-panel-container cyber-panel">
        <!-- 替换占位符为实际的FilterPanel组件 -->
        <FilterPanel />
        
        <div v-if="restaurantStore.loading" class="loading-indicator">
          <span class="neon-text-pink">数据加载中...</span>
        </div>
        <div v-else-if="restaurantStore.error" class="error-message">
          <span class="neon-text-yellow">{{ restaurantStore.error }}</span>
        </div>
        <div v-else class="restaurant-list">
          <h3 class="neon-text-cyan">餐厅列表</h3>
          <div 
            v-for="restaurant in restaurantStore.filteredRestaurants" 
            :key="restaurant.id"
            class="restaurant-item cyber-item"
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
  background-color: var(--cp-darker);
}

.cyber-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--cp-dark);
  color: var(--cp-light);
  padding: 0.5rem 1rem;
  height: 60px;
  box-shadow: 0 0 10px var(--cp-pink), 0 0 20px rgba(255, 42, 109, 0.3);
  border-bottom: 2px solid var(--cp-pink);
  position: relative;
  z-index: 20;
}

.cyber-header h1 {
  margin: 0;
  font-size: 1.5rem;
  letter-spacing: 2px;
  font-family: 'Orbitron', sans-serif;
}

.cyber-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--cp-cyan), var(--cp-pink), var(--cp-yellow));
  opacity: 0.8;
  animation: scan-line 3s linear infinite;
}

.cyber-link {
  color: var(--cp-light);
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  margin-left: 0.5rem;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
}

.cyber-link:hover {
  color: var(--cp-cyan);
  text-shadow: 0 0 5px var(--cp-cyan);
}

.cyber-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--cp-cyan);
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.cyber-link:hover::before {
  transform: scaleX(1);
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

.cyber-panel {
  width: 320px;
  background-color: rgba(26, 26, 26, 0.8);
  border-right: 1px solid var(--cp-pink);
  box-shadow: inset -2px 0 5px rgba(255, 42, 109, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 5;
  position: relative;
  overflow: hidden;
}

.cyber-panel::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 1px;
  height: 100%;
  background: var(--cp-pink);
  opacity: 0.8;
  box-shadow: 0 0 10px var(--cp-pink);
}

.loading-indicator {
  padding: 2rem;
  text-align: center;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

.error-message {
  padding: 1rem;
  margin: 1rem;
  border: 1px solid var(--cp-yellow);
  box-shadow: 0 0 5px var(--cp-yellow);
  animation: glitch 1s infinite;
}

@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

.restaurant-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 1rem;
  scrollbar-width: thin;
  scrollbar-color: var(--cp-pink) var(--cp-dark);
}

.restaurant-list::-webkit-scrollbar {
  width: 8px;
}

.restaurant-list::-webkit-scrollbar-track {
  background: var(--cp-dark);
}

.restaurant-list::-webkit-scrollbar-thumb {
  background-color: var(--cp-pink);
  border-radius: 0;
}

.restaurant-list h3 {
  margin: 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--cp-cyan);
  letter-spacing: 1px;
  text-transform: uppercase;
  font-family: 'Orbitron', sans-serif;
}

.cyber-item {
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  cursor: pointer;
  border-left: 3px solid transparent;
  background-color: rgba(26, 26, 26, 0.6);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.cyber-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background-color: var(--cp-cyan);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.cyber-item:hover {
  background-color: rgba(5, 217, 232, 0.1);
}

.cyber-item:hover::before {
  opacity: 1;
}

.cyber-item.active {
  background-color: rgba(5, 217, 232, 0.15);
  border-left-color: var(--cp-cyan);
  box-shadow: 0 0 10px rgba(5, 217, 232, 0.2);
}

.cyber-item.active::before {
  opacity: 1;
  box-shadow: 0 0 5px var(--cp-cyan);
}

.restaurant-name {
  font-weight: 600;
  color: var(--cp-light);
  margin-bottom: 0.25rem;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
}

.restaurant-meta {
  display: flex;
  font-size: 0.8rem;
  color: var(--cp-cyan);
  justify-content: space-between;
  opacity: 0.8;
}

.map-wrapper {
  flex: 1;
  position: relative;
}

@media (max-width: 768px) {
  .cyber-panel {
    position: absolute;
    width: 85%;
    max-width: 320px;
    z-index: 100;
    height: 100%;
    transform: translateX(-100%);
    transition: transform 0.3s ease-out;
  }
  
  .cyber-panel.active {
    transform: translateX(0);
  }
}
</style> 