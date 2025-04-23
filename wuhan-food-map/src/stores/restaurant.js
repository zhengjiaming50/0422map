import { defineStore } from 'pinia'
import { restaurantApi } from '../services/api'

export const useRestaurantStore = defineStore('restaurant', {
  // 状态
  state: () => ({
    restaurants: [],
    filteredRestaurants: [],
    selectedRestaurant: null,
    loading: false,
    error: null,
    filters: {
      district: '',
      foodType: '',
      searchQuery: ''
    },
    districtList: [],
    foodTypeList: [],
    // 添加区域框选相关状态
    boxSelection: {
      active: false,
      restaurants: [],
      bounds: null
    },
    // 添加热力图相关状态
    heatmap: {
      active: false,
      data: null
    },
    // 添加统计数据状态
    stats: {
      byDistrict: [],
      byFoodType: []
    }
  }),

  // 计算属性
  getters: {
    getRestaurantById: (state) => (id) => {
      return state.restaurants.find(restaurant => restaurant.id === id)
    },
    
    getRestaurantsByDistrict: (state) => (district) => {
      if (!district) return state.restaurants
      return state.restaurants.filter(restaurant => restaurant.district === district)
    },
    
    getRestaurantsByFoodType: (state) => (foodType) => {
      if (!foodType) return state.restaurants
      return state.restaurants.filter(restaurant => restaurant.food_type === foodType)
    }
  },

  // 操作方法
  actions: {
    // 获取所有餐厅数据
    async fetchRestaurants() {
      this.loading = true
      this.error = null
      
      try {
        // 调用API服务获取餐厅数据
        const restaurantsData = await restaurantApi.getRestaurants({
          district: this.filters.district,
          foodType: this.filters.foodType,
          query: this.filters.searchQuery
        })
        
        this.restaurants = restaurantsData
        this.filteredRestaurants = restaurantsData
        
        // 同时获取区域和美食类型列表
        if (this.districtList.length === 0) {
          this.fetchDistrictList()
        }
        
        if (this.foodTypeList.length === 0) {
          this.fetchFoodTypeList()
        }
      } catch (error) {
        this.error = error.message || '获取餐厅数据失败'
        console.error('获取餐厅数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    // 获取餐厅详情
    async fetchRestaurantDetails(id) {
      if (!id) return
      
      try {
        // 先检查是否已有详细数据
        const existingRestaurant = this.getRestaurantById(id)
        if (existingRestaurant && existingRestaurant.description) {
          this.selectedRestaurant = existingRestaurant
          return existingRestaurant
        }
        
        // 否则获取详细数据
        const restaurantData = await restaurantApi.getRestaurantById(id)
        
        // 更新餐厅列表中的数据
        const index = this.restaurants.findIndex(r => r.id === id)
        if (index !== -1) {
          this.restaurants[index] = restaurantData
        }
        
        this.selectedRestaurant = restaurantData
        return restaurantData
      } catch (error) {
        console.error(`获取餐厅详情失败 (ID: ${id}):`, error)
        throw error
      }
    },
    
    // 获取区域列表
    async fetchDistrictList() {
      try {
        this.districtList = await restaurantApi.getDistricts()
      } catch (error) {
        console.error('获取区域列表失败:', error)
      }
    },
    
    // 获取美食类型列表
    async fetchFoodTypeList() {
      try {
        this.foodTypeList = await restaurantApi.getFoodTypes()
      } catch (error) {
        console.error('获取美食类型列表失败:', error)
      }
    },
    
    // 应用筛选条件
    async applyFilters(filterOptions) {
      this.filters = { ...this.filters, ...filterOptions }
      
      // 重新获取数据
      await this.fetchRestaurants()
    },
    
    // 重置所有筛选条件
    async resetFilters() {
      this.filters = {
        district: '',
        foodType: '',
        searchQuery: ''
      }
      
      // 重新获取数据
      await this.fetchRestaurants()
    },
    
    // 设置选中的餐厅
    setSelectedRestaurant(restaurant) {
      this.selectedRestaurant = restaurant
    },
    
    // 清除选中的餐厅
    clearSelectedRestaurant() {
      this.selectedRestaurant = null
    },
    
    // 获取边界框内的餐厅
    async fetchRestaurantsInBox(bounds) {
      this.loading = true
      this.error = null
      
      try {
        // 保存当前边界框
        this.boxSelection.bounds = bounds
        
        // 获取边界框内的餐厅
        const boxRestaurants = await restaurantApi.getRestaurantsInBoundingBox(bounds)
        
        // 更新框选餐厅列表
        this.boxSelection.restaurants = boxRestaurants
        this.boxSelection.active = true
        
        return boxRestaurants
      } catch (error) {
        this.error = error.message || '获取区域内餐厅失败'
        console.error('获取区域内餐厅失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 清除框选
    clearBoxSelection() {
      this.boxSelection.active = false
      this.boxSelection.restaurants = []
      this.boxSelection.bounds = null
    },
    
    // 获取热力图数据
    async fetchHeatmapData() {
      this.loading = true
      this.error = null
      
      try {
        // 调用API获取热力图数据
        const heatmapData = await restaurantApi.getHeatmapData()
        
        // 更新状态
        this.heatmap.data = heatmapData
        
        return heatmapData
      } catch (error) {
        this.error = error.message || '获取热力图数据失败'
        console.error('获取热力图数据失败:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    // 切换热力图状态
    toggleHeatmap() {
      this.heatmap.active = !this.heatmap.active
      
      // 如果激活热力图但没有数据，则获取数据
      if (this.heatmap.active && !this.heatmap.data) {
        this.fetchHeatmapData()
      }
    },
    
    // 获取按区域统计的餐厅数量
    async fetchRestaurantStatsByDistrict() {
      this.loading = true
      this.error = null
      
      try {
        const statsByDistrict = await restaurantApi.getRestaurantStatsByDistrict()
        this.stats.byDistrict = statsByDistrict
        return statsByDistrict
      } catch (error) {
        this.error = error.message || '获取区域统计数据失败'
        console.error('获取区域统计数据失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    // 获取按美食类型统计的餐厅数量
    async fetchRestaurantStatsByFoodType() {
      this.loading = true
      this.error = null
      
      try {
        const statsByFoodType = await restaurantApi.getRestaurantStatsByFoodType()
        this.stats.byFoodType = statsByFoodType
        return statsByFoodType
      } catch (error) {
        this.error = error.message || '获取美食类型统计数据失败'
        console.error('获取美食类型统计数据失败:', error)
        return []
      } finally {
        this.loading = false
      }
    }
  }
}) 