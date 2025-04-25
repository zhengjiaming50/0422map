<template>
  <div 
    class="marker-container" 
    :class="{ 'active': isActive }" 
    @click="handleClick"
  >
    <div class="marker-icon cyber-marker">
      <span>🍜</span>
      <div class="marker-glow"></div>
    </div>
    <div v-if="showTooltip" class="marker-tooltip cyber-tooltip">
      {{ restaurant.name }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

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

onMounted(() => {
  const markerElement = document.querySelector('.marker-container');
  if (markerElement) {
    markerElement.addEventListener('mouseenter', handleMouseEnter);
    markerElement.addEventListener('mouseleave', handleMouseLeave);
  }
});

onUnmounted(() => {
  const markerElement = document.querySelector('.marker-container');
  if (markerElement) {
    markerElement.removeEventListener('mouseenter', handleMouseEnter);
    markerElement.removeEventListener('mouseleave', handleMouseLeave);
  }
});
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

.cyber-marker {
  background-color: var(--cp-dark);
  color: white;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  position: relative;
  transition: all 0.2s ease;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  border: 2px solid var(--cp-pink);
  box-shadow: 0 0 10px var(--cp-pink), inset 0 0 5px var(--cp-pink);
}

.marker-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  animation: pulse-glow 2s infinite alternate;
  pointer-events: none;
  opacity: 0.5;
  background: radial-gradient(ellipse at center, var(--cp-pink) 0%, transparent 70%);
}

@keyframes pulse-glow {
  0% {
    opacity: 0.3;
    transform: scale(0.95);
  }
  100% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

.cyber-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(13, 13, 13, 0.9);
  color: var(--cp-cyan);
  padding: 5px 10px;
  white-space: nowrap;
  font-size: 0.8rem;
  margin-bottom: 8px;
  z-index: 3;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  border: 1px solid var(--cp-cyan);
  box-shadow: 0 0 5px var(--cp-cyan);
  text-shadow: 0 0 5px var(--cp-cyan);
}

.cyber-tooltip:after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: var(--cp-cyan) transparent transparent transparent;
}

.active .cyber-marker {
  background-color: rgba(255, 42, 109, 0.8);
  transform: scale(1.1);
  border-color: var(--cp-cyan);
  box-shadow: 0 0 15px var(--cp-cyan), inset 0 0 10px var(--cp-cyan);
}

.active .marker-glow {
  background: radial-gradient(ellipse at center, var(--cp-cyan) 0%, transparent 70%);
  animation: pulse-glow-active 1.5s infinite alternate;
}

@keyframes pulse-glow-active {
  0% {
    opacity: 0.5;
    transform: scale(0.95);
  }
  100% {
    opacity: 0.9;
    transform: scale(1.1);
  }
}
</style> 