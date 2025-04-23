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
    
    <!-- 评价表单 -->
    <div class="review-form-container">
      <button v-if="!showReviewForm" @click="showReviewForm = true" class="write-review-btn">
        写评价
      </button>
      
      <form v-else class="review-form" @submit.prevent="submitReview">
        <div class="form-header">
          <h5>你的评价</h5>
          <button type="button" class="cancel-btn" @click="cancelReview">取消</button>
        </div>
        
        <div class="rating-input">
          <label>评分:</label>
          <div class="stars-input">
            <span 
              v-for="i in 5" 
              :key="i" 
              class="star" 
              :class="{ 'filled': i <= newReview.rating }"
              @click="newReview.rating = i"
            >★</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="userName">用户名 (可选):</label>
          <input 
            type="text" 
            id="userName" 
            v-model="newReview.user_name" 
            placeholder="匿名用户"
            class="form-control"
          >
        </div>
        
        <div class="form-group">
          <label for="comment">评价内容 (可选):</label>
          <textarea 
            id="comment" 
            v-model="newReview.comment" 
            placeholder="分享你的用餐体验..." 
            class="form-control"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            type="submit" 
            class="submit-btn" 
            :disabled="!newReview.rating || isSubmitting"
          >
            {{ isSubmitting ? '提交中...' : '提交评价' }}
          </button>
        </div>
      </form>
    </div>
    
    <!-- 评价列表 -->
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
const isSubmitting = ref(false);
const showReviewForm = ref(false);

// 新评价数据
const newReview = ref({
  rating: 0,
  comment: '',
  user_name: ''
});

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

// 提交评价
const submitReview = async () => {
  if (!newReview.value.rating) return;
  
  isSubmitting.value = true;
  try {
    await restaurantApi.submitReview(props.restaurantId, newReview.value);
    
    // 重置表单
    newReview.value = { rating: 0, comment: '', user_name: '' };
    showReviewForm.value = false;
    
    // 重新获取评价列表
    await fetchReviews();
    
  } catch (error) {
    console.error('提交评价失败:', error);
    alert('提交评价失败: ' + error.message);
  } finally {
    isSubmitting.value = false;
  }
};

// 取消评价
const cancelReview = () => {
  newReview.value = { rating: 0, comment: '', user_name: '' };
  showReviewForm.value = false;
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
  cursor: pointer;
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

/* 表单样式 */
.review-form-container {
  margin-bottom: 20px;
}

.write-review-btn {
  background-color: #457b9d;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  margin-bottom: 15px;
}

.write-review-btn:hover {
  background-color: #2a6f97;
}

.review-form {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.form-header h5 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.cancel-btn {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 0.9rem;
}

.cancel-btn:hover {
  color: #333;
  text-decoration: underline;
}

.rating-input {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.rating-input label {
  margin-right: 10px;
  font-weight: 600;
  color: #555;
}

.stars-input {
  display: flex;
}

.stars-input .star {
  font-size: 1.5rem;
  margin-right: 5px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

.form-control {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

textarea.form-control {
  resize: vertical;
}

.form-actions {
  text-align: right;
}

.submit-btn {
  background-color: #e63946;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:hover:not(:disabled) {
  background-color: #c1121f;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style> 