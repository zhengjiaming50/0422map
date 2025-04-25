<template>
  <div class="filter-panel">
    <div class="panel-section">
      <div class="section-title">区</div>
      <div class="section-content">
        <select v-model="selectedDistrict" class="filter-select" @change="applyFilters">
          <option value="">以下区域 为所有美食店铺</option>
          <option v-for="district in districtList" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="panel-section">
      <div class="section-title">美食类型</div>
      <div class="section-content">
        <select v-model="selectedFoodType" class="filter-select" @change="applyFilters">
          <option value="">所有类型</option>
          <option v-for="foodType in foodTypeList" :key="foodType" :value="foodType">
            {{ foodType }}
          </option>
        </select>
      </div>
    </div>

    <div class="description-section">
      <p>点击任意店铺，会在地图上缩放到对应店铺，并且在地图上点击该店铺会出现店铺详情</p>
    </div>
    
    <div class="filter-actions">
      <button class="reset-btn" @click="resetFilters">重置筛选</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'

// 餐厅状态管理
const restaurantStore = useRestaurantStore()

// 响应式状态
const searchQuery = ref('')
const selectedDistrict = ref('')
const selectedFoodType = ref('')

// 计算属性
const districtList = computed(() => restaurantStore.districtList)
const foodTypeList = computed(() => restaurantStore.foodTypeList)

// 防抖搜索定时器
let searchTimer = null
const debounceSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    applySearch()
  }, 500) // 延迟500毫秒执行搜索
}

// 应用筛选条件
const applyFilters = async () => {
  await restaurantStore.applyFilters({
    district: selectedDistrict.value,
    foodType: selectedFoodType.value,
    searchQuery: searchQuery.value
  })
}

// 应用搜索
const applySearch = async () => {
  await restaurantStore.applyFilters({
    district: selectedDistrict.value,
    foodType: selectedFoodType.value,
    searchQuery: searchQuery.value
  })
}

// 重置所有筛选条件
const resetFilters = async () => {
  searchQuery.value = ''
  selectedDistrict.value = ''
  selectedFoodType.value = ''
  
  await restaurantStore.resetFilters()
}

// 初始化
onMounted(async () => {
  // 如果还没有区域和美食类型列表，则获取它们
  if (districtList.value.length === 0) {
    await restaurantStore.fetchDistrictList()
  }
  
  if (foodTypeList.value.length === 0) {
    await restaurantStore.fetchFoodTypeList()
  }
})

// 当筛选条件在store中更新时，同步到组件
watch(() => restaurantStore.filters, (newFilters) => {
  searchQuery.value = newFilters.searchQuery || ''
  selectedDistrict.value = newFilters.district || ''
  selectedFoodType.value = newFilters.foodType || ''
}, { deep: true })
</script>

<style scoped>
.filter-panel {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #8B4513;
  color: white;
  height: 100%;
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-title {
  background-color: #4369b2;
  padding: 0.5rem 1rem;
  font-weight: bold;
  text-align: center;
}

.section-content {
  padding: 0.5rem;
}

.filter-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  color: #333;
  font-size: 0.9rem;
}

.description-section {
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 0.9rem;
}

.filter-actions {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.reset-btn {
  padding: 0.5rem 1rem;
  background-color: #4369b2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.reset-btn:hover {
  background-color: #365b99;
}
</style> 