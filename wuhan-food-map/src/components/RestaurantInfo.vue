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
    
    <div class="info-reviews">
      <h4>用户评价</h4>
      
      <div v-if="reviews.length > 0" class="rating-summary">
        <div class="average-rating">
          <span class="rating-number">{{ averageRating.toFixed(1) }}</span>
          <div class="stars">
            <span 
              v-for="n in 5" 
              :key="n" 
              :class="{ 'star-filled': n <= Math.round(averageRating), 'star': n > Math.round(averageRating) }"
            >★</span>
          </div>
        </div>
        <div class="rating-count">{{ reviews.length }}条评价</div>
      </div>
      <div v-else class="no-reviews">暂无评价</div>
      
      <div v-if="reviews.length > 0" class="review-list">
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <div class="review-header">
            <div class="review-stars">
              <span v-for="n in 5" :key="n" :class="{ 'star-filled': n <= review.rating, 'star': n > review.rating }">★</span>
            </div>
            <div class="review-user">{{ review.user_name || '匿名用户' }}</div>
            <div class="review-date">{{ formatDate(review.created_at) }}</div>
          </div>
          <div v-if="review.comment" class="review-comment">
            {{ review.comment }}
          </div>
        </div>
      </div>
      
      <div class="add-review">
        <h5>添加评价</h5>
        
        <div class="rating-selector">
          <span>你的评分:</span>
          <div class="rating-stars">
            <span 
              v-for="n in 5" 
              :key="n" 
              :class="{ 'star-filled': n <= newReview.rating, 'star': n > newReview.rating }" 
              @click="setRating(n)"
            >★</span>
          </div>
        </div>
        
        <div class="review-form">
          <input 
            type="text" 
            v-model="newReview.user_name" 
            placeholder="你的昵称（可选）" 
            class="review-input"
          />
          <textarea 
            v-model="newReview.comment" 
            placeholder="说说你的体验（可选）" 
            class="review-textarea"
          ></textarea>
          <button 
            class="submit-review" 
            @click="submitReview"
            :disabled="!newReview.rating || submitting"
          >
            {{ submitting ? '提交中...' : '提交评价' }}
          </button>
        </div>
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
import { ref, computed, onMounted } from 'vue';
import { restaurantApi } from '../services/api';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

const reviews = ref([]);
const loading = ref(false);
const error = ref(null);
const submitting = ref(false);

const newReview = ref({
  rating: 0,
  comment: '',
  user_name: ''
});

const averageRating = computed(() => {
  if (reviews.value.length === 0) return 0;
  const sum = reviews.value.reduce((total, review) => total + review.rating, 0);
  return sum / reviews.value.length;
});

const fetchReviews = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    reviews.value = await restaurantApi.getRestaurantReviews(props.restaurant.id);
  } catch (err) {
    console.error('获取评价失败:', err);
    error.value = '无法加载评价';
  } finally {
    loading.value = false;
  }
};

const setRating = (rating) => {
  newReview.value.rating = rating;
};

const submitReview = async () => {
  if (!newReview.value.rating) return;
  
  submitting.value = true;
  
  try {
    await restaurantApi.addRestaurantReview(props.restaurant.id, newReview.value);
    await fetchReviews();
    newReview.value = {
      rating: 0,
      comment: '',
      user_name: ''
    };
  } catch (err) {
    console.error('提交评价失败:', err);
  } finally {
    submitting.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
};

const navigateTo = () => {
  console.log('导航到:', props.restaurant.name);
};

onMounted(() => {
  fetchReviews();
});
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

.info-reviews {
  padding: 15px;
  border-top: 1px solid #eee;
}

.info-reviews h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1rem;
  color: #333;
}

.rating-summary {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.average-rating {
  display: flex;
  align-items: center;
}

.rating-number {
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 10px;
  color: #f1c40f;
}

.stars {
  display: flex;
}

.star, .star-filled {
  color: #ddd;
  font-size: 1.2rem;
}

.star-filled {
  color: #f1c40f;
}

.rating-count {
  margin-left: 10px;
  color: #777;
  font-size: 0.9rem;
}

.no-reviews {
  color: #777;
  font-style: italic;
  margin-bottom: 15px;
}

.review-list {
  margin-bottom: 20px;
  max-height: 200px;
  overflow-y: auto;
}

.review-item {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.review-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 5px;
}

.review-stars {
  margin-right: 10px;
}

.review-user {
  font-weight: 600;
  margin-right: 10px;
}

.review-date {
  color: #777;
  font-size: 0.8rem;
}

.review-comment {
  color: #555;
  line-height: 1.4;
}

.add-review h5 {
  margin-top: 15px;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #555;
}

.rating-selector {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.rating-selector span {
  margin-right: 10px;
  color: #555;
}

.rating-stars span {
  cursor: pointer;
  font-size: 1.5rem;
}

.review-form {
  display: flex;
  flex-direction: column;
}

.review-input, .review-textarea {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.review-textarea {
  min-height: 80px;
  resize: vertical;
}

.submit-review {
  background-color: #1d3557;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.submit-review:hover {
  background-color: #264a73;
}

.submit-review:disabled {
  background-color: #aaa;
  cursor: not-allowed;
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