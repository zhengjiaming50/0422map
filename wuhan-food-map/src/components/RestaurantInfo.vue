<template>
  <div class="restaurant-info-popup">
    <div class="popup-header">
      <h3>店铺详情弹出窗口: 内容如下:</h3>
    </div>
    
    <div class="popup-content">
      <div class="info-item">
        <div class="item-label">餐厅详情（即点击地图上的餐厅会弹出餐厅的营业时间，电话，特色菜以及用户评价）</div>
      </div>
      
      <div v-if="restaurant.phone" class="info-item">
        <div class="item-label">电话:</div>
        <div class="item-value">{{ restaurant.phone }}</div>
      </div>
      
      <div v-if="restaurant.special_dish" class="info-item">
        <div class="item-label">特色菜:</div>
        <div class="item-value">{{ restaurant.special_dish || restaurant.description }}</div>
      </div>
      
      <!-- 用户评价部分 -->
      <div class="review-section">
        <div class="item-label">用户评价:</div>
        <RestaurantReviews :restaurant-id="restaurant.id" />
        
        <div class="rating-button-container">
          <button class="rating-btn" @click="showRatingForm">我要评价</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import RestaurantReviews from './RestaurantReviews.vue';
import { ref } from 'vue';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

const showRatingForm = () => {
  // 实现评价表单逻辑
  console.log('打开评价表单:', props.restaurant.name);
};
</script>

<style scoped>
.restaurant-info-popup {
  background-color: #4369b2;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 320px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
  color: white;
}

.popup-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.popup-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}

.popup-content {
  padding: 15px;
}

.info-item {
  margin-bottom: 15px;
}

.item-label {
  font-weight: 600;
  margin-bottom: 5px;
}

.item-value {
  color: #eee;
}

.review-section {
  margin-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding-top: 15px;
}

.rating-button-container {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}

.rating-btn {
  background-color: #8B4513;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.rating-btn:hover {
  background-color: #704214;
}
</style> 