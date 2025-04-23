<template>
  <div class="box-selection-list" v-if="active">
    <div class="box-header">
      <h3>框选区域内的餐厅 ({{ restaurants.length }})</h3>
      <button class="close-btn" @click="closeSelection">×</button>
    </div>
    
    <div class="restaurant-list" v-if="restaurants.length > 0">
      <div 
        v-for="restaurant in restaurants" 
        :key="restaurant.id"
        class="restaurant-item"
        @click="selectRestaurant(restaurant)"
      >
        <div class="restaurant-icon">🍜</div>
        <div class="restaurant-info">
          <h4>{{ restaurant.name }}</h4>
          <div class="restaurant-type">{{ restaurant.food_type || '未分类' }}</div>
          <div class="restaurant-address">{{ restaurant.address }}</div>
        </div>
      </div>
    </div>
    
    <div class="empty-list" v-else>
      <p>该区域内没有餐厅</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'

const restaurantStore = useRestaurantStore()

// 计算属性
const active = computed(() => restaurantStore.boxSelection.active)
const restaurants = computed(() => restaurantStore.boxSelection.restaurants)

// 方法
const closeSelection = () => {
  restaurantStore.clearBoxSelection()
  emit('close')
}

const selectRestaurant = (restaurant) => {
  restaurantStore.setSelectedRestaurant(restaurant)
  emit('select-restaurant', restaurant)
}

// 定义事件
const emit = defineEmits(['close', 'select-restaurant'])
</script>

<style scoped>
.box-selection-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  width: 350px;
  max-height: 500px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 5;
}

.box-header {
  padding: 12px 16px;
  background-color: #4369b2;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.restaurant-list {
  overflow-y: auto;
  padding: 8px 0;
  flex: 1;
}

.restaurant-item {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.restaurant-item:hover {
  background-color: #f5f7fa;
}

.restaurant-item:last-child {
  border-bottom: none;
}

.restaurant-icon {
  margin-right: 12px;
  font-size: 24px;
}

.restaurant-info {
  flex: 1;
}

.restaurant-info h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
  color: #333;
}

.restaurant-type {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.restaurant-address {
  font-size: 12px;
  color: #888;
}

.empty-list {
  padding: 20px;
  text-align: center;
  color: #666;
}
</style> 