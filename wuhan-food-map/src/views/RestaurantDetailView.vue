<template>
  <div class="restaurant-detail-view">
    <header class="detail-header">
      <h1>餐厅详情</h1>
      <div class="nav-links">
        <router-link to="/map" class="back-link">返回地图</router-link>
        <router-link to="/" class="home-link">返回首页</router-link>
      </div>
    </header>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchData" class="retry-btn">重试</button>
    </div>
    
    <div v-else-if="restaurant" class="restaurant-detail-container">
      <div class="restaurant-header">
        <h2>{{ restaurant.name }}</h2>
        <div class="restaurant-tags">
          <span class="tag food-type">{{ restaurant.food_type || '未知类型' }}</span>
          <span class="tag district">{{ restaurant.district || '未知区域' }}</span>
        </div>
      </div>
      
      <div class="restaurant-image-container">
        <img :src="restaurantImage" :alt="restaurant.name" class="restaurant-image">
      </div>
      
      <div class="restaurant-info-container">
        <div class="info-section">
          <h3>基本信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">地址：</span>
              <span class="info-value">{{ restaurant.address }}</span>
            </div>
            <div class="info-item" v-if="restaurant.phone">
              <span class="info-label">电话：</span>
              <span class="info-value">{{ restaurant.phone }}</span>
            </div>
            <div class="info-item" v-if="restaurant.business_hours">
              <span class="info-label">营业时间：</span>
              <span class="info-value">{{ restaurant.business_hours }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">经纬度：</span>
              <span class="info-value">{{ restaurant.longitude }}, {{ restaurant.latitude }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="restaurant.description" class="info-section">
          <h3>餐厅介绍</h3>
          <p class="restaurant-description">{{ restaurant.description }}</p>
        </div>
        
        <div class="info-section">
          <h3>用户评价</h3>
          <RestaurantReviews :restaurant-id="restaurant.id" />
        </div>
      </div>
      
      <div class="action-buttons">
        <button class="action-btn back-to-map" @click="backToMap">
          <span>在地图上查看</span>
        </button>
      </div>
    </div>
    
    <div v-else class="not-found-container">
      <p>未找到餐厅信息</p>
      <router-link to="/map" class="back-btn">返回地图</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useRestaurantStore } from '../stores/restaurant';
import RestaurantReviews from '../components/RestaurantReviews.vue';

// 导入所有餐厅图片
import restaurant1Img from '../assets/images/restaurant_1.jpg';
import restaurant2Img from '../assets/images/restaurant_2.jpg';
import restaurant3Img from '../assets/images/restaurant_3.jpg';
import restaurant4Img from '../assets/images/restaurant_4.jpg';
import restaurant5Img from '../assets/images/restaurant_5.jpg';
import restaurant6Img from '../assets/images/restaurant_6.jpg';
import restaurant7Img from '../assets/images/restaurant_7.jpg';
import restaurant8Img from '../assets/images/restaurant_8.jpg';
import restaurant9Img from '../assets/images/restaurant_9.jpg';
import restaurant10Img from '../assets/images/restaurant_10.jpg';
import restaurant11Img from '../assets/images/restaurant_11.jpg';
import restaurant12Img from '../assets/images/restaurant_12.jpg';
import restaurant13Img from '../assets/images/restaurant_13.jpg';
import restaurant14Img from '../assets/images/restaurant_14.jpg';
import restaurant15Img from '../assets/images/restaurant_15.jpg';
import restaurant16Img from '../assets/images/restaurant_16.jpg';
import restaurant17Img from '../assets/images/restaurant_17.jpg';
import restaurant18Img from '../assets/images/restaurant_18.jpg';
import restaurant19Img from '../assets/images/restaurant_19.jpg';
import restaurant20Img from '../assets/images/restaurant_20.jpg';

const route = useRoute();
const router = useRouter();
const restaurantStore = useRestaurantStore();

const restaurant = ref(null);
const loading = ref(true);
const error = ref(null);

// 计算图片路径 - 根据餐厅ID选择对应图片
const restaurantImage = computed(() => {
  if (!restaurant.value) return restaurant1Img;
  
  // 创建餐厅ID到图片的映射
  const imageMap = {
    1: restaurant1Img,
    2: restaurant2Img,
    3: restaurant3Img,
    4: restaurant4Img,
    5: restaurant5Img,
    6: restaurant6Img,
    7: restaurant7Img,
    8: restaurant8Img,
    9: restaurant9Img,
    10: restaurant10Img,
    11: restaurant11Img,
    12: restaurant12Img,
    13: restaurant13Img,
    14: restaurant14Img,
    15: restaurant15Img,
    16: restaurant16Img,
    17: restaurant17Img,
    18: restaurant18Img,
    19: restaurant19Img,
    20: restaurant20Img,
  };
  
  // 获取餐厅ID对应的图片，如果ID不在1-20范围内，则使用餐厅ID对1-20取模后的图片
  const id = restaurant.value.id;
  if (id >= 1 && id <= 20) {
    return imageMap[id];
  } else {
    // 对于ID超过20的餐厅，使用ID对20取模后的图片（确保在1-20之间）
    const mappedId = ((id - 1) % 20) + 1;
    return imageMap[mappedId];
  }
});

// 获取餐厅数据
const fetchData = async () => {
  loading.value = true;
  error.value = null;

  try {
    const restaurantId = Number(route.params.id);
    if (isNaN(restaurantId)) {
      throw new Error('无效的餐厅ID');
    }

    const result = await restaurantStore.fetchRestaurantDetails(restaurantId);
    restaurant.value = result;
  } catch (err) {
    console.error('获取餐厅详情失败:', err);
    error.value = '获取餐厅信息失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 返回地图并定位到该餐厅
const backToMap = () => {
  // 先保存当前选中的餐厅，以便地图页面可以获取
  restaurantStore.setSelectedRestaurant(restaurant.value);
  router.push('/map');
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.restaurant-detail-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #e63946;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.back-link, .home-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.back-link:hover, .home-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.loading-container, .error-container, .not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  height: 60vh;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #e63946;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #e63946;
  font-weight: 500;
  margin-bottom: 1rem;
}

.retry-btn, .back-btn {
  background-color: #e63946;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

.restaurant-detail-container {
  max-width: 800px;
  margin: 2rem auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.restaurant-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.restaurant-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
  color: #1d3557;
}

.restaurant-tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.food-type {
  background-color: #e9f5db;
  color: #588157;
}

.district {
  background-color: #d8f3dc;
  color: #2d6a4f;
}

.restaurant-image-container {
  height: 300px;
  width: 100%;
  overflow: hidden;
}

.restaurant-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.restaurant-info-container {
  padding: 1.5rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: #1d3557;
  border-bottom: 2px solid #e63946;
  padding-bottom: 0.5rem;
  display: inline-block;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-label {
  font-weight: 600;
  color: #555;
  margin-bottom: 0.25rem;
}

.info-value {
  color: #333;
}

.restaurant-description {
  line-height: 1.6;
  color: #555;
}

.action-buttons {
  padding: 1.5rem;
  display: flex;
  justify-content: center;
  border-top: 1px solid #eee;
}

.action-btn {
  background-color: #457b9d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background-color: #1d3557;
}
</style> 