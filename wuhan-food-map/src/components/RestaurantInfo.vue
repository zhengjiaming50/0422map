<template>
  <div class="restaurant-info cyber-panel">
    <div class="info-header">
      <h3 class="neon-text">{{ restaurant.name }}</h3>
      <button class="close-btn cyber-btn-small" @click="$emit('close')">X</button>
    </div>
    
    <!-- 测试简化的图片区域 -->
    <div style="border: 1px solid red; padding: 5px; margin: 5px">
      <p>测试图片：</p>
      <img :src="testImage" alt="测试图片" style="max-width: 100px">
      <p>餐厅图片路径: {{ restaurant.image_url }}</p>
    </div>
    
    <div class="info-image cyber-image">
      <img :src="displayImage" :alt="restaurant.name">
      <div class="cyber-scan-line"></div>
    </div>
    
    <div class="info-content">
      <div class="info-item cyber-item">
        <div class="item-label">类型:</div>
        <div class="item-value neon-text-cyan">{{ restaurant.food_type || '未知' }}</div>
      </div>
      
      <div class="info-item cyber-item">
        <div class="item-label">区域:</div>
        <div class="item-value neon-text-cyan">{{ restaurant.district || '未知' }}</div>
      </div>
      
      <div class="info-item cyber-item">
        <div class="item-label">地址:</div>
        <div class="item-value">{{ restaurant.address }}</div>
      </div>
      
      <div v-if="restaurant.phone" class="info-item cyber-item">
        <div class="item-label">电话:</div>
        <div class="item-value">{{ restaurant.phone }}</div>
      </div>
      
      <div v-if="restaurant.business_hours" class="info-item cyber-item">
        <div class="item-label">营业时间:</div>
        <div class="item-value">{{ restaurant.business_hours }}</div>
      </div>
    </div>
    
    <div v-if="restaurant.description" class="info-description">
      <h4 class="neon-text-pink">餐厅介绍</h4>
      <p>{{ restaurant.description }}</p>
    </div>
    
    <!-- 用户评价部分 -->
    <RestaurantReviews :restaurant-id="restaurant.id" />
    
    <div class="info-actions">
      <button class="cyber-btn" @click="navigateTo">
        <span>导航到这里</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import RestaurantReviews from './RestaurantReviews.vue';
import { ref, computed, onMounted } from 'vue';
import testImage from '@/assets/test.jpg';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

// 使用计算属性确定要显示的图片
const displayImage = computed(() => {
  // 获取餐厅图片路径
  const imagePath = props.restaurant.image_url;
  
  // 如果没有图片路径，返回测试图片
  if (!imagePath) {
    console.log('无图片路径，使用默认图片');
    return testImage;
  }
  
  // 检查图片路径是否以http开头，如果是则直接使用该路径
  if (imagePath.startsWith('http')) {
    return imagePath;
  }
  
  // 否则将路径解析为相对于public目录的路径
  return imagePath;
});

// 组件挂载后输出调试信息
onMounted(() => {
  console.log('餐厅信息组件已挂载');
  console.log('餐厅数据:', props.restaurant);
  console.log('图片路径:', props.restaurant.image_url);
  console.log('显示图片:', displayImage.value);
});

const navigateTo = () => {
  // 以后实现导航功能
  console.log('导航到:', props.restaurant.name);
  // 可以使用百度地图、高德地图等第三方导航服务
};
</script>

<style scoped>
.restaurant-info {
  background-color: rgba(26, 26, 26, 0.9);
  width: 350px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
  border: 1px solid var(--cp-pink);
  box-shadow: 0 0 15px var(--cp-pink), inset 0 0 10px rgba(255, 42, 109, 0.3);
  scrollbar-width: thin;
  scrollbar-color: var(--cp-pink) var(--cp-dark);
  color: var(--cp-light);
}

.restaurant-info::-webkit-scrollbar {
  width: 5px;
}

.restaurant-info::-webkit-scrollbar-track {
  background: var(--cp-dark);
}

.restaurant-info::-webkit-scrollbar-thumb {
  background-color: var(--cp-pink);
  border-radius: 0;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid var(--cp-pink);
  background-color: var(--cp-dark);
  position: relative;
}

.info-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, var(--cp-cyan), var(--cp-pink));
  opacity: 0.8;
}

.info-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'Orbitron', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.cyber-btn-small {
  background: transparent;
  border: 1px solid var(--cp-pink);
  color: var(--cp-pink);
  font-size: 0.9rem;
  cursor: pointer;
  padding: 5px 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.cyber-btn-small:hover {
  background-color: var(--cp-pink);
  color: var(--cp-dark);
  box-shadow: 0 0 8px var(--cp-pink);
}

.cyber-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.cyber-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(1.2) contrast(1.1);
}

.cyber-scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    transparent 50%,
    rgba(5, 217, 232, 0.1) 50%
  );
  background-size: 100% 4px;
  z-index: 1;
  pointer-events: none;
}

.info-content {
  padding: 15px;
  background-color: rgba(13, 13, 13, 0.7);
}

.cyber-item {
  display: flex;
  margin-bottom: 10px;
  padding: 8px;
  background-color: rgba(26, 26, 26, 0.5);
  border-left: 2px solid var(--cp-cyan);
  transition: all 0.2s;
}

.cyber-item:hover {
  background-color: rgba(5, 217, 232, 0.1);
  box-shadow: 0 0 5px rgba(5, 217, 232, 0.2);
}

.item-label {
  font-weight: 600;
  color: var(--cp-light);
  width: 80px;
  flex-shrink: 0;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
}

.item-value {
  color: var(--cp-light);
  flex-grow: 1;
  font-family: 'Rajdhani', sans-serif;
}

.info-description {
  padding: 0 15px 15px;
  border-top: 1px solid rgba(5, 217, 232, 0.3);
  margin-top: 10px;
}

.info-description h4 {
  margin-top: 15px;
  margin-bottom: 8px;
  font-size: 1rem;
  font-family: 'Orbitron', sans-serif;
  letter-spacing: 1px;
}

.info-description p {
  margin: 0;
  color: var(--cp-light);
  line-height: 1.5;
  font-family: 'Rajdhani', sans-serif;
}

.info-actions {
  padding: 15px;
  display: flex;
  justify-content: center;
  border-top: 1px solid rgba(5, 217, 232, 0.3);
}

.cyber-btn {
  background-color: transparent;
  color: var(--cp-light);
  border: 2px solid var(--cp-cyan);
  padding: 10px 15px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 10px var(--cp-cyan), inset 0 0 10px var(--cp-cyan);
}

.cyber-btn:hover {
  background-color: var(--cp-cyan);
  color: var(--cp-dark);
  text-shadow: none;
}
</style> 