<template>
  <div class="food-culture-view">
    <h1 class="page-title">武汉美食文化</h1>
    
    <!-- 筛选部分 -->
    <div class="filter-container">
      <div class="filter-group">
        <label>美食类型:</label>
        <select v-model="selectedFoodType" @change="applyFilters">
          <option value="">所有类型</option>
          <option v-for="type in foodTypes" :key="type" :value="type">{{ type }}</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>发源地区:</label>
        <select v-model="selectedDistrict" @change="applyFilters">
          <option value="">所有地区</option>
          <option v-for="district in originDistricts" :key="district" :value="district">{{ district }}</option>
        </select>
      </div>
      
      <button class="reset-btn" @click="resetFilters">重置筛选</button>
    </div>
    
    <!-- 加载中状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>正在加载美食文化数据...</p>
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error-container">
      <p>加载失败: {{ error }}</p>
      <button @click="fetchData">重试</button>
    </div>
    
    <!-- 内容展示 -->
    <div v-else class="content-container">
      <!-- 美食文化卡片展示 -->
      <div v-if="!selectedFoodCulture" class="food-culture-grid">
        <div 
          v-for="food in filteredFoodCultures" 
          :key="food.id" 
          class="food-culture-card"
          @click="showFoodCultureDetails(food.id)"
        >
          <div class="card-image">
            <img :src="food.image_url || 'default-food.jpg'" :alt="food.name">
          </div>
          <div class="card-content">
            <h3>{{ food.name }}</h3>
            <p class="food-type">{{ food.food_type }}</p>
            <p class="food-district">{{ food.origin_district }}</p>
            <p class="food-description">{{ truncateText(food.description, 100) }}</p>
          </div>
        </div>
      </div>
      
      <!-- 美食文化详情 -->
      <div v-else class="food-culture-detail">
        <button class="back-btn" @click="clearSelectedFoodCulture">返回列表</button>
        
        <div class="detail-header">
          <h2>{{ selectedFoodCulture.name }}</h2>
          <p class="food-type">{{ selectedFoodCulture.food_type }}</p>
          <p class="food-district">发源地: {{ selectedFoodCulture.origin_district }}</p>
        </div>
        
        <div class="detail-image">
          <img :src="selectedFoodCulture.image_url || 'default-food.jpg'" :alt="selectedFoodCulture.name">
        </div>
        
        <div class="detail-section">
          <h3>简介</h3>
          <p>{{ selectedFoodCulture.description }}</p>
        </div>
        
        <div class="detail-section">
          <h3>历史背景</h3>
          <p>{{ selectedFoodCulture.history }}</p>
        </div>
        
        <div class="detail-section">
          <h3>制作方法</h3>
          <p>{{ selectedFoodCulture.making_method }}</p>
        </div>
        
        <div v-if="selectedFoodCulture.restaurants && selectedFoodCulture.restaurants.length > 0" class="detail-section">
          <h3>推荐餐厅</h3>
          <ul class="restaurant-list">
            <li v-for="restaurant in selectedFoodCulture.restaurants" :key="restaurant.id">
              <a @click="goToRestaurant(restaurant.id)">{{ restaurant.name }}</a> - {{ restaurant.district }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFoodCultureStore } from '../stores/foodCulture'

export default {
  name: 'FoodCultureView',
  
  setup() {
    const router = useRouter()
    const foodCultureStore = useFoodCultureStore()
    
    const selectedFoodType = ref('')
    const selectedDistrict = ref('')
    
    // 计算属性
    const loading = computed(() => foodCultureStore.loading)
    const error = computed(() => foodCultureStore.error)
    const foodTypes = computed(() => foodCultureStore.foodTypes)
    const originDistricts = computed(() => foodCultureStore.originDistricts)
    const filteredFoodCultures = computed(() => {
      let result = foodCultureStore.foodCultures
      
      if (selectedFoodType.value) {
        result = result.filter(food => food.food_type === selectedFoodType.value)
      }
      
      if (selectedDistrict.value) {
        result = result.filter(food => food.origin_district === selectedDistrict.value)
      }
      
      return result
    })
    const selectedFoodCulture = computed(() => foodCultureStore.selectedFoodCulture)
    
    // 方法
    const fetchData = async () => {
      await foodCultureStore.fetchFoodCultures()
      await foodCultureStore.fetchFoodTypes()
      await foodCultureStore.fetchOriginDistricts()
    }
    
    const applyFilters = () => {
      foodCultureStore.setFilter('foodType', selectedFoodType.value)
      foodCultureStore.setFilter('district', selectedDistrict.value)
      foodCultureStore.fetchFoodCultures()
    }
    
    const resetFilters = () => {
      selectedFoodType.value = ''
      selectedDistrict.value = ''
      foodCultureStore.resetFilters()
      foodCultureStore.fetchFoodCultures()
    }
    
    const showFoodCultureDetails = async (id) => {
      await foodCultureStore.fetchFoodCultureById(id)
    }
    
    const clearSelectedFoodCulture = () => {
      foodCultureStore.clearSelectedFoodCulture()
    }
    
    const truncateText = (text, maxLength) => {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    }
    
    const goToRestaurant = (id) => {
      router.push(`/map?restaurant=${id}`)
    }
    
    // 生命周期钩子
    onMounted(() => {
      fetchData()
    })
    
    return {
      loading,
      error,
      foodTypes,
      originDistricts,
      selectedFoodType,
      selectedDistrict,
      filteredFoodCultures,
      selectedFoodCulture,
      fetchData,
      applyFilters,
      resetFilters,
      showFoodCultureDetails,
      clearSelectedFoodCulture,
      truncateText,
      goToRestaurant
    }
  }
}
</script>

<style scoped>
.food-culture-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #D32F2F;
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: bold;
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.reset-btn {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #D32F2F;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 50px 0;
  color: #D32F2F;
}

.food-culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.food-culture-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
  background-color: white;
}

.food-culture-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.card-image {
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 15px;
}

.card-content h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #D32F2F;
}

.food-type, .food-district {
  display: inline-block;
  margin-right: 10px;
  padding: 4px 8px;
  background-color: #FFCDD2;
  color: #B71C1C;
  border-radius: 4px;
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.food-description {
  color: #666;
  line-height: 1.5;
}

.food-culture-detail {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-btn {
  margin-bottom: 20px;
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.back-btn:hover {
  background-color: #e0e0e0;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-header h2 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #D32F2F;
}

.detail-image {
  width: 100%;
  max-height: 400px;
  overflow: hidden;
  margin-bottom: 20px;
  border-radius: 8px;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #D32F2F;
  border-bottom: 2px solid #FFCDD2;
  padding-bottom: 5px;
}

.detail-section p {
  line-height: 1.6;
}

.restaurant-list {
  list-style-type: none;
  padding: 0;
}

.restaurant-list li {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.restaurant-list a {
  color: #D32F2F;
  cursor: pointer;
  text-decoration: none;
}

.restaurant-list a:hover {
  text-decoration: underline;
}
</style> 