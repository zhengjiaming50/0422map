<template>
  <div class="restaurant-info">
    <div class="info-header">
      <h3>{{ restaurant.name }}</h3>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </div>
    
    <div class="info-image">
      <!-- 主图片加载 - 确保有足够的CSS规则使图片显示 -->
      <img v-if="!imageLoadFailed && imageUrl" 
           :src="imageUrl" 
           :alt="restaurant.name" 
           @error="handleImageError" 
           @load="handleImageLoaded"
           class="main-image"
           style="display: block; width: 100%; height: 100%; object-fit: cover;">
      
      <!-- 备用显示方式：Base64 编码的图片显示 -->
      <img v-if="fallbackBase64 && loadingMethod === 'base64'" 
           :src="fallbackBase64" 
           :alt="restaurant.name"
           class="fallback-image"
           style="display: block; width: 100%; height: 100%; object-fit: cover;">
          
      <!-- 图片加载状态显示 -->
      <div v-if="imageStatus !== 'loaded'" class="image-loading" :class="{'image-error': imageLoadFailed}">
        <div class="status-icon" :class="imageStatus"></div>
        <p>{{ imageStatusText }}</p>
        <p v-if="debugInfo" class="debug-info">{{ debugInfo }}</p>
        
        <!-- 调试工具栏 -->
        <div class="debug-toolbar">
          <button @click="reloadImage" class="debug-btn">重试加载</button>
          <button @click="tryDefaultImage" class="debug-btn">使用默认图</button>
          <button @click="toggleImageInfo" class="debug-btn">{{ showImageInfo ? '隐藏' : '显示' }}详细信息</button>
          <button @click="switchLoadingMethod" class="debug-btn">切换加载方式</button>
        </div>
        
        <!-- 图片详细信息 -->
        <div v-if="showImageInfo" class="image-debug-info">
          <p>食物类型: {{ restaurant.food_type || '未知' }}</p>
          <p>当前加载方式: {{ loadingMethod }}</p>
          <p>当前图片URL: {{ activeImageUrl }}</p>
          <p>当前尝试: {{ currentAttempt }}/{{ maxAttempts }}</p>
          <p>加载开始: {{ loadStartTime }}</p>
          <p>最后错误: {{ lastError }}</p>
        </div>
      </div>
      
      <!-- 图片实际加载成功但未显示的调试区 -->
      <div v-if="imageStatus === 'loaded' && !imageLoadFailed" class="image-debug-overlay">
        <button @click="toggleImageInfo" class="debug-btn debug-corner-btn">
          调试
        </button>
      </div>
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
    
    <!-- 用户评价部分 -->
    <RestaurantReviews :restaurant-id="restaurant.id" />
    
    <div class="info-actions">
      <button class="action-btn" @click="navigateTo">
        <span>导航到这里</span>
      </button>
      
      <router-link :to="`/restaurant/${restaurant.id}`" class="detail-btn">
        <span>查看详情</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import RestaurantReviews from './RestaurantReviews.vue';
import { ref, computed, onMounted, watch } from 'vue';

// 导入所有餐厅图片
import restaurant1Img from '../assets/images/restaurant_1.jpg';
import restaurant2Img from '../assets/images/restaurant_2.jpg';
import restaurant3Img from '../assets/images/restaurant_3.jpg';
import restaurant4Img from '../assets/images/restaurant_4.jpg';
import restaurant5Img from '../assets/images/restaurant_5.jpg';
import restaurant6Img from '../assets/images/restaurant_6.jpg';
import restaurant7Img from '../assets/images/restaurant_7.jpg';
import restaurant8Img from '../assets/images/restaurant_8.jpg';
import restaurant9Img from '../assets/images/restaurant_9.jpg';
import restaurant10Img from '../assets/images/restaurant_10.jpg';
import restaurant11Img from '../assets/images/restaurant_11.jpg';
import restaurant12Img from '../assets/images/restaurant_12.jpg';
import restaurant13Img from '../assets/images/restaurant_13.jpg';
import restaurant14Img from '../assets/images/restaurant_14.jpg';
import restaurant15Img from '../assets/images/restaurant_15.jpg';
import restaurant16Img from '../assets/images/restaurant_16.jpg';
import restaurant17Img from '../assets/images/restaurant_17.jpg';
import restaurant18Img from '../assets/images/restaurant_18.jpg';
import restaurant19Img from '../assets/images/restaurant_19.jpg';
import restaurant20Img from '../assets/images/restaurant_20.jpg';

// 图片加载状态
const imageStatus = ref('loading'); // loading, error, loaded
const imageLoadFailed = ref(false);
const loadStartTime = ref('');
const currentAttempt = ref(0);
const maxAttempts = 3;
const lastError = ref('');
const debugInfo = ref('');
const showImageInfo = ref(false);
const fallbackBase64 = ref(null);
const imagePaths = ref({});
const activeImageUrl = ref('');
const loadingMethod = ref('import'); // 'import', 'relative', 'absolute', 'base64'

// 图片加载状态文本
const imageStatusText = computed(() => {
  switch (imageStatus.value) {
    case 'loading': return `加载图片中 (${loadingMethod.value}方式)...`;
    case 'error': return '图片加载失败';
    case 'loaded': return '图片加载成功';
    default: return '未知状态';
  }
});

const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

// 创建ID和图片的映射表
const imageIdMap = {
  1: restaurant1Img,
  2: restaurant2Img,
  3: restaurant3Img,
  4: restaurant4Img,
  5: restaurant5Img,
  6: restaurant6Img,
  7: restaurant7Img,
  8: restaurant8Img,
  9: restaurant9Img,
  10: restaurant10Img,
  11: restaurant11Img,
  12: restaurant12Img,
  13: restaurant13Img,
  14: restaurant14Img,
  15: restaurant15Img,
  16: restaurant16Img,
  17: restaurant17Img,
  18: restaurant18Img,
  19: restaurant19Img,
  20: restaurant20Img,
};

// 计算图片路径（根据ID选择图片）
const imagePath = computed(() => {
  const id = props.restaurant.id;
  let mappedId = id;
  
  // 对于超过20的ID，对20取模以保证在1-20范围内
  if (id > 20) {
    mappedId = ((id - 1) % 20) + 1;
  }
  
  // 保存映射信息用于调试
  Object.keys(imageIdMap).forEach(key => {
    imagePaths.value[key] = String(imageIdMap[key]);
  });
  
  return imageIdMap[mappedId] || imageIdMap[1]; // 默认使用第一张图片
});

// 获取相对路径地址
const relativeImageUrl = computed(() => {
  const id = props.restaurant.id;
  const mappedId = id > 20 ? ((id - 1) % 20) + 1 : id;
  return `./assets/images/restaurant_${mappedId}.jpg`;
});

// 获取绝对路径地址
const absoluteImageUrl = computed(() => {
  const id = props.restaurant.id;
  const mappedId = id > 20 ? ((id - 1) % 20) + 1 : id;
  return `/src/assets/images/restaurant_${mappedId}.jpg`;
});

// 直接计算当前使用的图片URL
const imageUrl = computed(() => {
  // 根据当前尝试的方法返回不同的URL
  switch(loadingMethod.value) {
    case 'import': return imagePath.value;
    case 'relative': return relativeImageUrl.value;
    case 'absolute': return absoluteImageUrl.value;
    case 'base64': return fallbackBase64.value;
    default: return imagePath.value;
  }
});

// 处理图片加载成功
const handleImageLoaded = () => {
  console.log('图片加载成功:', {
    url: activeImageUrl.value,
    method: loadingMethod.value,
    element: document.querySelector('.main-image')?.getBoundingClientRect()
  });
  
  imageStatus.value = 'loaded';
  imageLoadFailed.value = false;
  debugInfo.value = `成功加载 (${loadingMethod.value}): ${new Date().toLocaleTimeString()}`;
  
  // 强制触发DOM更新
  setTimeout(() => {
    const img = document.querySelector('.main-image');
    if (img) {
      // 设置特定样式确保图片可见
      img.style.display = 'block';
      img.style.visibility = 'visible';
      img.style.opacity = '1';
    }
  }, 100);
};

// 处理图片加载错误
const handleImageError = (event) => {
  currentAttempt.value++;
  const errorDetails = {
    url: activeImageUrl.value,
    method: loadingMethod.value,
    time: new Date().toLocaleTimeString(),
    attempt: currentAttempt.value,
    restaurantId: props.restaurant.id,
    eventType: event.type
  };
  
  console.error('图片加载失败:', errorDetails);
  lastError.value = JSON.stringify(errorDetails);
  
  if (currentAttempt.value < maxAttempts) {
    // 尝试切换至下一种加载方法
    switchLoadingMethod();
    debugInfo.value = `加载失败，尝试${loadingMethod.value}方式加载`;
    setTimeout(reloadImage, 500);
  } else {
    imageStatus.value = 'error';
    imageLoadFailed.value = true;
    debugInfo.value = `所有加载方法都失败，请检查资源文件或网络`;
    
    // 尝试生成备用图片
    generateFallbackImage();
  }
};

// 切换图片加载方式
const switchLoadingMethod = () => {
  const methods = ['import', 'relative', 'absolute', 'base64'];
  const currentIndex = methods.indexOf(loadingMethod.value);
  const nextIndex = (currentIndex + 1) % methods.length;
  loadingMethod.value = methods[nextIndex];
  console.log(`切换到${loadingMethod.value}加载方式`);
};

// 重新加载图片
const reloadImage = () => {
  imageStatus.value = 'loading';
  debugInfo.value = `正在使用${loadingMethod.value}方式重新加载...`;
  loadStartTime.value = new Date().toLocaleTimeString();
  
  // 更新当前激活的URL
  activeImageUrl.value = imageUrl.value;
  
  // 强制刷新图片
  setTimeout(() => {
    const imgElement = document.querySelector('.main-image');
    if (imgElement) {
      imgElement.src = 'about:blank';
      setTimeout(() => {
        const newUrl = imageUrl.value + (imageUrl.value.includes('?') ? '&' : '?') + 't=' + new Date().getTime();
        imgElement.src = newUrl;
        console.log('重新加载图片:', newUrl);
      }, 50);
    }
  }, 50);
};

// 尝试使用默认图片
const tryDefaultImage = () => {
  console.log('尝试使用默认图片');
  imageStatus.value = 'loading';
  debugInfo.value = '尝试加载默认图片...';
  currentAttempt.value = 0;
  loadingMethod.value = 'import';
  
  // 直接使用默认图片
  const imgElement = document.querySelector('.main-image');
  if (imgElement) {
    imgElement.src = imagePath.value;
    activeImageUrl.value = imagePath.value;
  }
};

// 生成备用图片 (使用 Canvas 生成文本图片作为备用)
const generateFallbackImage = () => {
  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 320;
    canvas.height = 180;
    
    // 背景
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 边框
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 2;
    ctx.strokeRect(5, 5, canvas.width - 10, canvas.height - 10);
    
    // 文字
    ctx.fillStyle = '#666';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(props.restaurant.name, canvas.width/2, 70);
    ctx.font = '14px Arial';
    ctx.fillText(`ID: ${props.restaurant.id}`, canvas.width/2, 100);
    ctx.font = '12px Arial';
    ctx.fillText('图片加载失败 - 替代显示', canvas.width/2, 130);
    
    // 转换为 base64
    fallbackBase64.value = canvas.toDataURL('image/png');
    loadingMethod.value = 'base64';
    console.log('已生成备用图片，使用base64显示');
    
    // 更新状态
    activeImageUrl.value = fallbackBase64.value;
    imageStatus.value = 'loaded'; // 将状态更改为已加载，因为我们已经有了可显示的内容
  } catch (error) {
    console.error('生成备用图片失败:', error);
    fallbackBase64.value = null;
  }
};

// 切换显示详细信息
const toggleImageInfo = () => {
  showImageInfo.value = !showImageInfo.value;
};

// 导航功能
const navigateTo = () => {
  console.log('导航到:', props.restaurant.name);
};

// 当餐厅ID变化时重置加载状态
watch(() => props.restaurant.id, () => {
  console.log('餐厅ID变更，重置图片加载状态');
  currentAttempt.value = 0;
  imageStatus.value = 'loading';
  imageLoadFailed.value = false;
  loadingMethod.value = 'import';
  loadStartTime.value = new Date().toLocaleTimeString();
  activeImageUrl.value = imagePath.value;
});

// 组件挂载时初始化
onMounted(() => {
  loadStartTime.value = new Date().toLocaleTimeString();
  activeImageUrl.value = imagePath.value;
  
  // 记录调试信息
  console.log('RestaurantInfo组件挂载，尝试加载图片:', {
    restaurant: props.restaurant.name,
    restaurantId: props.restaurant.id,
    imageUrl: imageUrl.value,
    domElement: document.querySelector('.info-image') ? '存在' : '不存在'
  });
  
  // 解析已导入图片的实际路径
  debugInfo.value = `准备加载图片: 餐厅ID ${props.restaurant.id}`;
  
  // 尝试直接通过DOM操作确保图片可见性
  setTimeout(() => {
    const imgElements = document.querySelectorAll('.info-image img');
    imgElements.forEach(img => {
      img.style.display = 'block';
      img.style.visibility = 'visible';
      img.style.opacity = '1';
    });
  }, 500);
  
  // 打印日志辅助调试
  console.log('图片路径映射：', imagePaths.value);
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
  position: relative;
  background-color: #f5f5f5;
}

.info-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.image-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  color: #666;
  font-size: 0.9rem;
  text-align: center;
  padding: 20px;
  z-index: 5;
}

.image-error {
  background-color: #fff0f0;
}

.debug-info {
  font-size: 0.8rem;
  color: #999;
  margin-top: 5px;
  word-break: break-all;
  max-width: 100%;
}

.status-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.status-icon.loading {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  animation: spin 1s linear infinite;
}

.status-icon.error {
  background-color: #e74c3c;
  position: relative;
}

.status-icon.error:before,
.status-icon.error:after {
  content: '';
  position: absolute;
  width: 24px;
  height: 4px;
  background-color: white;
  top: 18px;
  left: 8px;
}

.status-icon.error:before {
  transform: rotate(45deg);
}

.status-icon.error:after {
  transform: rotate(-45deg);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.debug-toolbar {
  display: flex;
  gap: 5px;
  margin-top: 10px;
}

.debug-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 3px;
  padding: 4px 8px;
  font-size: 0.8rem;
  cursor: pointer;
}

.debug-btn:hover {
  background-color: #e0e0e0;
}

.image-debug-info {
  margin-top: 10px;
  background-color: rgba(0,0,0,0.05);
  padding: 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  text-align: left;
  max-width: 90%;
}

.image-debug-info p {
  margin: 2px 0;
  color: #666;
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

.detail-btn {
  background-color: #457b9d;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.2s;
  margin-left: 10px;
  display: inline-block;
}

.detail-btn:hover {
  background-color: #1d3557;
}

.fallback-image {
  border: 1px dashed #ccc;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
}

.image-debug-overlay {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 10;
}

.debug-corner-btn {
  margin: 5px;
  background-color: rgba(0,0,0,0.5);
  color: white;
  border: none;
  font-size: 0.7rem;
  border-radius: 3px;
  padding: 3px 6px;
  cursor: pointer;
}
</style> 