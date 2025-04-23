<template>
  <div class="restaurant-info">
    <div class="info-header">
      <h3>{{ restaurant.name }}</h3>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </div>
    
    <div v-if="restaurant.image_url" class="info-image">
      <img :src="restaurant.image_url" :alt="restaurant.name">
    </div>
    
    <div class="info-content">
      <div v-if="reviewData" class="rating-summary">
        <RatingStars :model-value="reviewData.avg_rating" />
        <span class="rating-text">{{ reviewData.avg_rating.toFixed(1) }} ({{ reviewData.review_count }})</span>
      </div>
      
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
    
    <div class="info-actions">
      <button class="action-btn" @click="navigateTo">
        <span>导航到这里</span>
      </button>
    </div>
    
    <!-- 用户评价区域 -->
    <div class="info-reviews">
      <div class="section-heading">
        <h4>用户评价</h4>
        <button v-if="!showReviewForm" class="add-review-btn" @click="showReviewForm = true">
          写评价
        </button>
      </div>
      
      <ReviewForm 
        v-if="showReviewForm" 
        :restaurant-id="restaurant.id" 
        :on-success="handleReviewSubmit"
      />
      
      <ReviewList 
        :reviews="reviews" 
        :avg-rating="reviewData?.avg_rating || 0" 
        :review-count="reviewData?.review_count || 0"
        :loading="isLoading" 
        :error="error"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { restaurantApi } from '../services/api';
import RatingStars from './RatingStars.vue';
import ReviewList from './ReviewList.vue';
import ReviewForm from './ReviewForm.vue';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

// 评价数据
const reviews = ref([]);
const reviewData = ref(null);
const isLoading = ref(false);
const error = ref('');
const showReviewForm = ref(false);

// 获取评价数据
const fetchReviews = async () => {
  if (!props.restaurant || !props.restaurant.id) return;
  
  isLoading.value = true;
  error.value = '';
  
  try {
    const data = await restaurantApi.getRestaurantReviews(props.restaurant.id);
    reviews.value = data.reviews;
    reviewData.value = {
      avg_rating: data.avg_rating,
      review_count: data.review_count
    };
  } catch (err) {
    console.error('获取评价失败:', err);
    error.value = '无法加载评价数据';
  } finally {
    isLoading.value = false;
  }
};

// 提交评价
const handleReviewSubmit = async (reviewData) => {
  if (!props.restaurant || !props.restaurant.id) return;
  
  // 提交评价
  await restaurantApi.addRestaurantReview(props.restaurant.id, reviewData);
  
  // 重新获取评价列表
  await fetchReviews();
  
  // 隐藏评价表单
  showReviewForm.value = false;
};

// 导航功能
const navigateTo = () => {
  // 以后实现导航功能
  console.log('导航到:', props.restaurant.name);
  // 可以使用百度地图、高德地图等第三方导航服务
};

// 组件加载时获取评价
onMounted(fetchReviews);
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

.rating-summary {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.rating-text {
  margin-left: 8px;
  color: #666;
  font-size: 0.9rem;
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

.info-reviews {
  padding: 15px;
  border-top: 1px solid #eee;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-heading h4 {
  margin: 0;
  color: #333;
}

.add-review-btn {
  background-color: #1d3557;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.add-review-btn:hover {
  background-color: #14253d;
}
</style> 