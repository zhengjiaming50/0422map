<template>
  <div class="reviews-container">
    <div class="reviews-header">
      <h4>用户评价 ({{ reviewsData.total_reviews || 0 }})</h4>
      <div class="avg-rating">
        <span class="stars">
          <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= Math.round(reviewsData.avg_rating) }">★</span>
        </span>
        <span class="rating-value">{{ reviewsData.avg_rating || 0 }}/5</span>
      </div>
    </div>
    
    <div v-if="reviewsData.reviews && reviewsData.reviews.length > 0" class="reviews-list">
      <div v-for="review in reviewsData.reviews" :key="review.id" class="review-item">
        <div class="review-header">
          <div class="user-info">
            <span class="user-name">{{ review.user_name || '匿名用户' }}</span>
            <span class="review-date">{{ formatDate(review.created_at) }}</span>
          </div>
          <div class="review-rating">
            <span v-for="i in 5" :key="i" class="star" :class="{ 'filled': i <= review.rating }">★</span>
          </div>
        </div>
        <div v-if="review.comment" class="review-comment">
          {{ review.comment }}
        </div>
      </div>
    </div>
    
    <div v-else class="no-reviews">
      <p>暂无评价</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { restaurantApi } from '../services/api';

const props = defineProps({
  restaurantId: {
    type: Number,
    required: true
  }
});

// 评价数据
const reviewsData = ref({
  reviews: [],
  avg_rating: 0,
  total_reviews: 0
});

// 加载状态
const isLoading = ref(false);

// 获取评价数据
const fetchReviews = async () => {
  if (!props.restaurantId) return;
  
  isLoading.value = true;
  try {
    const data = await restaurantApi.getRestaurantReviews(props.restaurantId);
    reviewsData.value = data;
  } catch (error) {
    console.error('获取评价失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

// 餐厅ID变化时重新获取评价
watch(() => props.restaurantId, (newVal) => {
  if (newVal) {
    fetchReviews();
  }
});

// 组件挂载时获取评价
onMounted(() => {
  if (props.restaurantId) {
    fetchReviews();
  }
});
</script>

<style scoped>
.reviews-container {
  padding: 15px;
  border-top: 1px solid #eee;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.reviews-header h4 {
  margin: 0;
  color: #333;
  font-size: 1rem;
}

.avg-rating {
  display: flex;
  align-items: center;
}

.stars {
  display: inline-flex;
  margin-right: 5px;
}

.star {
  color: #ddd;
  font-size: 1rem;
}

.star.filled {
  color: #f8ce0b;
}

.rating-value {
  font-size: 0.9rem;
  color: #555;
  font-weight: 600;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 300px;
  overflow-y: auto;
}

.review-item {
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
}

.review-date {
  font-size: 0.8rem;
  color: #777;
}

.review-rating {
  margin-left: 10px;
}

.review-comment {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #555;
  white-space: pre-line;
}

.no-reviews {
  text-align: center;
  padding: 20px 0;
  color: #777;
}
</style> 