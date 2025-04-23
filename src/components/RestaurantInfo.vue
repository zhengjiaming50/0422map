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
    
    <!-- 添加评价展示部分 -->
    <div class="reviews-section">
      <h4>用户评价</h4>
      <div v-if="loading" class="loading-indicator">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <div v-else-if="reviews.length === 0" class="no-reviews">
        暂无评价，做第一个评价的人吧！
      </div>
      <div v-else class="reviews-list">
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <div class="review-header">
            <div class="review-user">{{ review.user_name }}</div>
            <div class="review-rating">
              <span v-for="i in 5" :key="i" class="star">
                {{ i <= review.rating ? '★' : '☆' }}
              </span>
            </div>
          </div>
          <div class="review-date">{{ formatDate(review.created_at) }}</div>
          <div class="review-comment">{{ review.comment }}</div>
        </div>
      </div>
    </div>
    
    <!-- 添加评价提交表单 -->
    <div class="add-review-section">
      <h4>添加评价</h4>
      <div class="rating-input">
        <span>评分:</span>
        <div class="star-rating">
          <span 
            v-for="i in 5" 
            :key="i" 
            @click="newReview.rating = i"
            @mouseover="hoverRating = i"
            @mouseleave="hoverRating = 0"
            class="star-select"
          >
            {{ (hoverRating || newReview.rating) >= i ? '★' : '☆' }}
          </span>
        </div>
      </div>
      <div class="form-group">
        <label for="user-name">用户名:</label>
        <input 
          type="text" 
          id="user-name" 
          v-model="newReview.user_name" 
          placeholder="请输入用户名"
          class="form-input"
        >
      </div>
      <div class="form-group">
        <label for="comment">评价内容:</label>
        <textarea 
          id="comment" 
          v-model="newReview.comment" 
          placeholder="请分享您的用餐体验..."
          class="form-textarea"
        ></textarea>
      </div>
      <button 
        class="submit-review-btn" 
        @click="submitReview"
        :disabled="!isFormValid || submitting"
      >
        {{ submitting ? '提交中...' : '提交评价' }}
      </button>
      <div v-if="submitError" class="submit-error">
        {{ submitError }}
      </div>
      <div v-if="submitSuccess" class="submit-success">
        评价提交成功！
      </div>
    </div>
    
    <div class="info-actions">
      <button class="action-btn" @click="navigateTo">
        <span>导航到这里</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { getRestaurantReviews, addRestaurantReview } from '../services/api';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

// 评价数据
const reviews = ref([]);
const loading = ref(false);
const error = ref(null);

// 新评价表单
const newReview = ref({
  rating: 0,
  comment: '',
  user_name: ''
});
const hoverRating = ref(0);
const submitting = ref(false);
const submitError = ref(null);
const submitSuccess = ref(false);

// 表单验证
const isFormValid = computed(() => {
  return newReview.value.rating > 0 && 
         newReview.value.user_name.trim() !== '' && 
         newReview.value.comment.trim() !== '';
});

// 加载评价
const fetchReviews = async () => {
  if (!props.restaurant || !props.restaurant.id) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    reviews.value = await getRestaurantReviews(props.restaurant.id);
  } catch (err) {
    console.error('Failed to fetch reviews:', err);
    error.value = '无法加载评价，请稍后再试';
  } finally {
    loading.value = false;
  }
};

// 提交评价
const submitReview = async () => {
  if (!isFormValid.value) return;
  
  submitting.value = true;
  submitError.value = null;
  submitSuccess.value = false;
  
  try {
    const newReviewData = await addRestaurantReview(
      props.restaurant.id, 
      newReview.value
    );
    
    // 添加到评价列表
    reviews.value.unshift(newReviewData);
    
    // 重置表单
    newReview.value = {
      rating: 0,
      comment: '',
      user_name: ''
    };
    
    submitSuccess.value = true;
    
    // 3秒后隐藏成功消息
    setTimeout(() => {
      submitSuccess.value = false;
    }, 3000);
    
  } catch (err) {
    console.error('Failed to submit review:', err);
    submitError.value = '评价提交失败，请稍后再试';
  } finally {
    submitting.value = false;
  }
};

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 餐厅变化时加载评价
watch(() => props.restaurant?.id, (newId, oldId) => {
  if (newId && newId !== oldId) {
    fetchReviews();
  }
});

// 组件挂载时加载评价
onMounted(() => {
  if (props.restaurant?.id) {
    fetchReviews();
  }
});

const navigateTo = () => {
  // 导航到餐厅位置的方法(未实现完整功能)
  console.log('导航到餐厅:', props.restaurant.name);
};
</script>

<style scoped>
/* 保留原有样式 */

/* 评价部分样式 */
.reviews-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.reviews-list {
  max-height: 300px;
  overflow-y: auto;
}

.review-item {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
  margin-bottom: 0.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.review-user {
  font-weight: bold;
}

.review-rating {
  color: #e63946;
}

.review-date {
  font-size: 0.8rem;
  color: #777;
  margin-bottom: 0.5rem;
}

.star {
  display: inline-block;
  margin-right: 0.1rem;
}

.no-reviews {
  font-style: italic;
  color: #777;
  padding: 0.5rem 0;
}

/* 添加评价表单样式 */
.add-review-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.rating-input {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.star-rating {
  margin-left: 0.5rem;
}

.star-select {
  font-size: 1.2rem;
  cursor: pointer;
  color: #e63946;
  margin-right: 0.2rem;
}

.form-group {
  margin-bottom: 0.75rem;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-textarea {
  min-height: 80px;
  resize: vertical;
}

.submit-review-btn {
  background-color: #e63946;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.submit-review-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-error {
  color: #e63946;
  margin-top: 0.5rem;
}

.submit-success {
  color: #2a9d8f;
  margin-top: 0.5rem;
}

.loading-indicator, .error-message {
  padding: 0.5rem 0;
  color: #777;
}

.error-message {
  color: #e63946;
}
</style> 