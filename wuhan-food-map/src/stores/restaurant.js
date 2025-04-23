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
    foodTypeList: []
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
    }
  }
}) 