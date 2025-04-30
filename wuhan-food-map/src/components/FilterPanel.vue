<template>
  <div class="filter-panel">
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="搜索餐厅名称..."
        class="search-input"
        @input="debounceSearch"
      />
      <button class="search-btn" @click="applySearch">
        <span>🔍</span>
      </button>
    </div>
    
    <div class="filter-container">
      <div class="filter-group">
        <h4>区域筛选</h4>
        <select v-model="selectedDistrict" class="filter-select" @change="applyFilters">
          <option value="">所有区域</option>
          <option v-for="district in districtList" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <h4>美食类型</h4>
        <select v-model="selectedFoodType" class="filter-select" @change="applyFilters">
          <option value="">所有类型</option>
          <option v-for="foodType in foodTypeList" :key="foodType" :value="foodType">
            {{ foodType }}
          </option>
        </select>
      </div>
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
}

.search-container {
  display: flex;
  width: 100%;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #aaa;
  border-radius: 4px 0 0 4px;
  font-size: 1.05rem;
  color: #222;
}

.search-input::placeholder {
  color: #666;
}

.search-btn {
  padding: 0.5rem 0.75rem;
  background-color: #e63946;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 1.1rem;
}

.search-btn:hover {
  background-color: #d62839;
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #111;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #aaa;
  border-radius: 4px;
  background-color: white;
  font-size: 1.05rem;
  color: #222;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.reset-btn {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #aaa;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.05rem;
  font-weight: 500;
  transition: all 0.2s;
}

.reset-btn:hover {
  background-color: #e9ecef;
  color: #111;
}
</style> 