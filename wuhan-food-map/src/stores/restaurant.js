import { defineStore } from 'pinia'

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
        // 在实际项目中，这里会调用API服务
        // const response = await api.getRestaurants()
        // this.restaurants = response.data
        // 临时模拟数据
        setTimeout(() => {
          this.restaurants = this.filteredRestaurants = [
            { id: 1, name: '黄鹤楼小吃店', district: '武昌区', food_type: '湖北菜', latitude: 30.5433, longitude: 114.3008 }
          ]
          this.loading = false
        }, 500)
      } catch (error) {
        this.error = error.message || '获取餐厅数据失败'
        this.loading = false
      }
    },
    
    // 应用筛选条件
    applyFilters(filterOptions) {
      this.filters = { ...this.filters, ...filterOptions }
      
      // 筛选餐厅
      let result = [...this.restaurants]
      
      if (this.filters.district) {
        result = result.filter(restaurant => restaurant.district === this.filters.district)
      }
      
      if (this.filters.foodType) {
        result = result.filter(restaurant => restaurant.food_type === this.filters.foodType)
      }
      
      if (this.filters.searchQuery) {
        const query = this.filters.searchQuery.toLowerCase()
        result = result.filter(restaurant => 
          restaurant.name.toLowerCase().includes(query) || 
          (restaurant.description && restaurant.description.toLowerCase().includes(query))
        )
      }
      
      this.filteredRestaurants = result
    },
    
    // 重置所有筛选条件
    resetFilters() {
      this.filters = {
        district: '',
        foodType: '',
        searchQuery: ''
      }
      this.filteredRestaurants = [...this.restaurants]
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