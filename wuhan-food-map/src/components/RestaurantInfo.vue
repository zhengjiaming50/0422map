<template>
  <div class="restaurant-info">
    <div class="info-header">
      <h3>{{ restaurant.name }}</h3>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </div>
    
    <div class="info-image">
      <img :src="getLocalImage(restaurant.food_type)" :alt="restaurant.name">
    </div>
    
    <div class="info-content">
      <div class="info-item">
        <div class="item-label">类型:</div>
        <div class="item-value">{{ restaurant.food_type || '未知' }}</div>
      </div>
      
      <div class="info-item">
        <div class="item-label">区域:</div>
        <div class="item-value">{{ restaurant.district || '未知' }}</div>
      </div>
      
      <div class="info-item">
        <div class="item-label">地址:</div>
        <div class="item-value">{{ restaurant.address }}</div>
      </div>
      
      <div v-if="restaurant.phone" class="info-item">
        <div class="item-label">电话:</div>
        <div class="item-value">{{ restaurant.phone }}</div>
      </div>
      
      <div v-if="restaurant.business_hours" class="info-item">
        <div class="item-label">营业时间:</div>
        <div class="item-value">{{ restaurant.business_hours }}</div>
      </div>
    </div>
    
    <div v-if="restaurant.description" class="info-description">
      <h4>餐厅介绍</h4>
      <p>{{ restaurant.description }}</p>
    </div>
    
    <!-- 用户评价部分 -->
    <RestaurantReviews :restaurant-id="restaurant.id" />
    
    <div class="info-actions">
      <button class="action-btn" @click="navigateTo">
        <span>导航到这里</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import RestaurantReviews from './RestaurantReviews.vue';
import hubeiImg from '../assets/images/hubei.jpg';
import xiaochiImg from '../assets/images/xiaochi.jpg';
import cakeImg from '../assets/images/cake.jpg';
import bbqImg from '../assets/images/bbq.jpg';
import westernImg from '../assets/images/western.jpg';
import hotpotImg from '../assets/images/hotpot.jpg';
import cantonImg from '../assets/images/canton.jpg';
import defaultImg from '../assets/images/default-food.jpg';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

// 根据食物类型返回颜色
const getFoodTypeColor = (foodType) => {
  const colorMap = {
    '湖北菜': '#e63946',
    '小吃': '#f4a261',
    '糕点': '#e9c46a',
    '烧烤': '#d62828',
    '西餐': '#457b9d',
    '火锅': '#bc6c25',
    '粤菜': '#2a9d8f'
  };
  
  return colorMap[foodType] || '#6c757d';
};

// 根据食物类型返回表情符号
const getFoodTypeEmoji = (foodType) => {
  const emojiMap = {
    '湖北菜': '🍜',
    '小吃': '🥟',
    '糕点': '🍰',
    '烧烤': '🍢',
    '西餐': '🍔',
    '火锅': '🍲',
    '粤菜': '🥘'
  };
  
  return emojiMap[foodType] || '🍽️';
};

// 根据食物类型返回本地图片
const getLocalImage = (foodType) => {
  const imageMap = {
    '湖北菜': hubeiImg,
    '小吃': xiaochiImg,
    '糕点': cakeImg,
    '烧烤': bbqImg,
    '西餐': westernImg,
    '火锅': hotpotImg,
    '粤菜': cantonImg
  };
  
  return imageMap[foodType] || defaultImg;
};

const navigateTo = () => {
  // 以后实现导航功能
  console.log('导航到:', props.restaurant.name);
  // 可以使用百度地图、高德地图等第三方导航服务
};
</script>

<style scoped>
.restaurant-info {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 320px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  background-color: #1d3557;
  color: white;
  border-radius: 8px 8px 0 0;
}

.info-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.info-image {
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.info-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-content {
  padding: 15px;
}

.info-item {
  display: flex;
  margin-bottom: 10px;
}

.item-label {
  font-weight: 600;
  color: #555;
  width: 80px;
  flex-shrink: 0;
}

.item-value {
  color: #333;
  flex-grow: 1;
}

.info-description {
  padding: 0 15px 15px;
  border-top: 1px solid #eee;
}

.info-description h4 {
  margin-top: 15px;
  margin-bottom: 8px;
  font-size: 1rem;
  color: #333;
}

.info-description p {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

.info-actions {
  padding: 15px;
  display: flex;
  justify-content: center;
  border-top: 1px solid #eee;
}

.action-btn {
  background-color: #e63946;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background-color: #c1121f;
}
</style> 