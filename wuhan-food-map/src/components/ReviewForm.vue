<template>
  <div class="review-form">
    <h4>添加您的评价</h4>
    
    <div class="form-group">
      <label>您的评分:</label>
      <RatingStars 
        v-model="rating" 
        :interactive="true" 
        :show-value="true" 
      />
    </div>
    
    <div class="form-group">
      <label for="user-name">您的名字 (可选):</label>
      <input 
        type="text" 
        id="user-name" 
        v-model="userName" 
        placeholder="请输入您的名字"
        class="form-input"
      />
    </div>
    
    <div class="form-group">
      <label for="comment">评价内容 (可选):</label>
      <textarea 
        id="comment" 
        v-model="comment" 
        placeholder="分享您的用餐体验..."
        class="form-textarea"
        rows="3"
      ></textarea>
    </div>
    
    <div class="form-actions">
      <button 
        @click="submitReview" 
        :disabled="!isValid || isSubmitting"
        class="submit-btn"
      >
        {{ isSubmitting ? '提交中...' : '提交评价' }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import RatingStars from './RatingStars.vue';

const props = defineProps({
  restaurantId: {
    type: Number,
    required: true
  },
  onSuccess: {
    type: Function,
    default: () => {}
  }
});

const rating = ref(0);
const userName = ref('');
const comment = ref('');
const isSubmitting = ref(false);
const error = ref('');

const isValid = computed(() => rating.value > 0);

const submitReview = async () => {
  if (!isValid.value) {
    error.value = '请至少选择一个评分星级';
    return;
  }
  
  isSubmitting.value = true;
  error.value = '';
  
  try {
    // 准备评价数据
    const reviewData = {
      rating: rating.value,
      user_name: userName.value.trim() || undefined,
      comment: comment.value.trim() || undefined
    };
    
    // 调用API服务提交评价
    // 注意：此处需要使用提供的onSuccess函数，让父组件处理API调用
    await props.onSuccess(reviewData);
    
    // 重置表单
    rating.value = 0;
    userName.value = '';
    comment.value = '';
    
  } catch (err) {
    error.value = '提交评价失败，请稍后再试';
    console.error('提交评价失败:', err);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.review-form {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-top: 20px;
}

.review-form h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #1d3557;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  flex-direction: column;
}

.submit-btn {
  background-color: #1d3557;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #14253d;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #e63946;
  margin-top: 10px;
  font-size: 0.9rem;
}
</style> 