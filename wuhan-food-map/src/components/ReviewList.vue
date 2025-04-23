<template>
  <div class="review-list">
    <div v-if="loading" class="loading">
      加载评价中...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="reviews.length === 0" class="no-reviews">
      还没有评价，快来添加第一条评价吧！
    </div>
    
    <div v-else>
      <div class="review-summary">
        <div class="avg-rating">
          <span class="rating-value">{{ avgRating }}</span>
          <RatingStars :model-value="avgRating" />
        </div>
        <span class="review-count">共 {{ reviewCount }} 条评价</span>
      </div>
      
      <div class="review-items">
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <div class="review-header">
            <span class="user-name">{{ review.user_name || '匿名用户' }}</span>
            <div class="review-rating">
              <RatingStars :model-value="review.rating" />
            </div>
          </div>
          
          <div class="review-content">
            {{ review.comment || '该用户未填写评价内容' }}
          </div>
          
          <div class="review-time">
            {{ formatDate(review.created_at) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import RatingStars from './RatingStars.vue';

const props = defineProps({
  reviews: {
    type: Array,
    required: true
  },
  avgRating: {
    type: Number,
    default: 0
  },
  reviewCount: {
    type: Number,
    default: 0
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
});

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>

<style scoped>
.review-list {
  margin-top: 20px;
}

.loading, .error, .no-reviews {
  padding: 15px;
  text-align: center;
  color: #666;
}

.error {
  color: #e63946;
}

.review-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.avg-rating {
  display: flex;
  align-items: center;
}

.rating-value {
  font-size: 1.8rem;
  font-weight: bold;
  margin-right: 10px;
  color: #1d3557;
}

.review-count {
  color: #666;
  font-size: 0.9rem;
}

.review-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.review-item {
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #eee;
  background-color: white;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.user-name {
  font-weight: 600;
  color: #1d3557;
}

.review-content {
  color: #333;
  line-height: 1.5;
  margin-bottom: 10px;
}

.review-time {
  font-size: 0.8rem;
  color: #999;
  text-align: right;
}
</style> 