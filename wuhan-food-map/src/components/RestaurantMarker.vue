<template>
  <div 
    class="marker-container" 
    :class="{ 'active': isActive }" 
    @click="handleClick"
  >
    <div class="marker-icon">
      <span>🍜</span>
    </div>
    <div v-if="showTooltip" class="marker-tooltip">
      {{ restaurant.name }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['click']);
const showTooltip = ref(false);

const handleClick = () => {
  emit('click', props.restaurant);
};

const handleMouseEnter = () => {
  showTooltip.value = true;
};

const handleMouseLeave = () => {
  showTooltip.value = false;
};
</script>

<style scoped>
.marker-container {
  position: relative;
  cursor: pointer;
  z-index: 1;
  transition: transform 0.2s ease;
}

.marker-container:hover {
  z-index: 2;
  transform: scale(1.1);
}

.marker-icon {
  background-color: #e63946;
  color: white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  font-size: 1rem;
  transition: all 0.2s ease;
}

.marker-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  padding: 5px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
  font-size: 0.8rem;
  margin-bottom: 5px;
  z-index: 3;
}

.marker-tooltip:after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: white transparent transparent transparent;
}

.active .marker-icon {
  background-color: #1d3557;
  transform: scale(1.1);
  border-color: #ffd166;
}
</style> 