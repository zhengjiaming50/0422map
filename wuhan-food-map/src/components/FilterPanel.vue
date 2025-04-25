<template>
  <div class="filter-panel cyber-panel">
    <h3 class="panel-title neon-text-cyan">筛选面板</h3>
    
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="搜索餐厅名称..."
        class="search-input cyber-input"
        @input="debounceSearch"
      />
      <button class="search-btn cyber-btn-small" @click="applySearch">
        <span>搜索</span>
      </button>
    </div>
    
    <div class="filter-container">
      <div class="filter-group cyber-group">
        <h4 class="neon-text-pink">区域筛选</h4>
        <select v-model="selectedDistrict" class="filter-select cyber-select" @change="applyFilters">
          <option value="">所有区域</option>
          <option v-for="district in districtList" :key="district" :value="district">
            {{ district }}
          </option>
        </select>
      </div>
      
      <div class="filter-group cyber-group">
        <h4 class="neon-text-pink">美食类型</h4>
        <select v-model="selectedFoodType" class="filter-select cyber-select" @change="applyFilters">
          <option value="">所有类型</option>
          <option v-for="foodType in foodTypeList" :key="foodType" :value="foodType">
            {{ foodType }}
          </option>
        </select>
      </div>
    </div>
    
    <div class="filter-actions">
      <button class="reset-btn cyber-btn-alt" @click="resetFilters">重置筛选</button>
    </div>
    
    <div class="cyber-decoration">
      <div class="cyber-line"></div>
      <div class="cyber-corner top-left"></div>
      <div class="cyber-corner top-right"></div>
      <div class="cyber-corner bottom-left"></div>
      <div class="cyber-corner bottom-right"></div>
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
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  background-color: rgba(13, 13, 13, 0.85);
  position: relative;
  border-bottom: 1px solid var(--cp-pink);
  color: var(--cp-light);
}

.panel-title {
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 1.2rem;
  margin-top: 0;
  margin-bottom: 1rem;
  position: relative;
  display: inline-block;
}

.panel-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--cp-cyan), transparent);
}

.search-container {
  display: flex;
  width: 100%;
  position: relative;
}

.cyber-input {
  flex: 1;
  padding: 0.6rem;
  background-color: rgba(26, 26, 26, 0.9);
  border: 1px solid var(--cp-cyan);
  color: var(--cp-light);
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  box-shadow: 0 0 5px var(--cp-cyan);
  transition: all 0.3s;
}

.cyber-input:focus {
  outline: none;
  border-color: var(--cp-pink);
  box-shadow: 0 0 8px var(--cp-pink);
}

.cyber-input::placeholder {
  color: rgba(209, 247, 255, 0.5);
}

.search-btn {
  padding: 0.6rem 1rem;
  background-color: transparent;
  color: var(--cp-cyan);
  border: 1px solid var(--cp-cyan);
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
  box-shadow: 0 0 5px rgba(5, 217, 232, 0.3);
}

.search-btn:hover {
  background-color: var(--cp-cyan);
  color: var(--cp-dark);
  box-shadow: 0 0 10px var(--cp-cyan);
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.cyber-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  padding: 1rem;
  background-color: rgba(26, 26, 26, 0.5);
  border-left: 2px solid var(--cp-pink);
  position: relative;
}

.cyber-group::before {
  content: '';
  position: absolute;
  top: 0;
  left: -2px;
  width: 2px;
  height: 100%;
  background-color: var(--cp-pink);
  box-shadow: 0 0 8px var(--cp-pink);
}

.cyber-group h4 {
  margin: 0;
  font-size: 0.9rem;
  font-family: 'Orbitron', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.cyber-select {
  padding: 0.6rem;
  background-color: rgba(26, 26, 26, 0.9);
  border: 1px solid var(--cp-cyan);
  color: var(--cp-light);
  font-family: 'Rajdhani', sans-serif;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2305d9e8'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.2em;
  cursor: pointer;
}

.cyber-select:focus {
  outline: none;
  border-color: var(--cp-pink);
  box-shadow: 0 0 8px var(--cp-pink);
}

.cyber-select option {
  background-color: var(--cp-dark);
  color: var(--cp-light);
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.cyber-btn-alt {
  padding: 0.6rem 1.2rem;
  background-color: transparent;
  border: 1px solid var(--cp-yellow);
  color: var(--cp-yellow);
  cursor: pointer;
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s;
  box-shadow: 0 0 5px rgba(252, 238, 10, 0.3);
  position: relative;
  overflow: hidden;
}

.cyber-btn-alt:hover {
  background-color: var(--cp-yellow);
  color: var(--cp-dark);
  box-shadow: 0 0 10px var(--cp-yellow);
}

.cyber-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cyber-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, var(--cp-cyan), var(--cp-pink), transparent);
}

.cyber-corner {
  position: absolute;
  width: 6px;
  height: 6px;
  border: 1px solid var(--cp-pink);
}

.cyber-corner.top-left {
  top: 5px;
  left: 5px;
  border-right: none;
  border-bottom: none;
}

.cyber-corner.top-right {
  top: 5px;
  right: 5px;
  border-left: none;
  border-bottom: none;
}

.cyber-corner.bottom-left {
  bottom: 5px;
  left: 5px;
  border-right: none;
  border-top: none;
}

.cyber-corner.bottom-right {
  bottom: 5px;
  right: 5px;
  border-left: none;
  border-top: none;
}
</style> 