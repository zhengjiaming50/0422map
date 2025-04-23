<template>
  <div class="rating-stars">
    <div class="stars-container">
      <span 
        v-for="star in 5" 
        :key="star"
        class="star"
        :class="{
          'filled': (modelValue >= star || tempRating >= star),
          'interactive': interactive
        }"
        @click="interactive && updateRating(star)"
        @mouseover="interactive && setTempRating(star)"
        @mouseleave="interactive && resetTempRating()"
      >
        ★
      </span>
    </div>
    <span v-if="showValue" class="rating-value">{{ modelValue || tempRating || 0 }}/5</span>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  interactive: {
    type: Boolean,
    default: false
  },
  showValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const tempRating = ref(0);

const updateRating = (value) => {
  emit('update:modelValue', value);
};

const setTempRating = (value) => {
  tempRating.value = value;
};

const resetTempRating = () => {
  tempRating.value = 0;
};
</script>

<style scoped>
.rating-stars {
  display: flex;
  align-items: center;
}

.stars-container {
  display: flex;
}

.star {
  font-size: 1.2rem;
  color: #ddd;
  cursor: default;
  transition: color 0.2s ease;
}

.star.filled {
  color: #ffbb00;
}

.star.interactive {
  cursor: pointer;
}

.star.interactive:hover {
  transform: scale(1.1);
}

.rating-value {
  margin-left: 8px;
  font-size: 0.9rem;
  color: #666;
}
</style> 