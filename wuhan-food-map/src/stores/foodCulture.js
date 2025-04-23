import { defineStore } from 'pinia'
import { foodCultureApi } from '../services/api'

// 美食文化状态管理
export const useFoodCultureStore = defineStore('foodCulture', {
  state: () => ({
    // 美食文化列表
    foodCultures: [],
    // 当前选择的美食文化
    selectedFoodCulture: null,
    // 美食路线列表
    foodRoutes: [],
    // 当前选择的美食路线
    selectedFoodRoute: null,
    // 美食类型列表
    foodTypes: [],
    // 发源地区列表
    originDistricts: [],
    // 筛选条件
    filters: {
      foodType: '',
      district: ''
    },
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),
  
  getters: {
    // 获取过滤后的美食文化列表
    filteredFoodCultures() {
      return this.foodCultures
    },
    
    // 按美食类型分组的美食文化
    foodCulturesByType() {
      const grouped = {}
      this.foodCultures.forEach(fc => {
        if (!grouped[fc.food_type]) {
          grouped[fc.food_type] = []
        }
        grouped[fc.food_type].push(fc)
      })
      return grouped
    },
    
    // 获取按区域筛选的美食路线
    foodRoutesByDistrict() {
      const grouped = {}
      this.foodRoutes.forEach(route => {
        if (!grouped[route.district]) {
          grouped[route.district] = []
        }
        grouped[route.district].push(route)
      })
      return grouped
    }
  },
  
  actions: {
    // 加载美食文化列表
    async fetchFoodCultures() {
      this.loading = true
      this.error = null
      
      try {
        this.foodCultures = await foodCultureApi.getFoodCultures(this.filters)
      } catch (error) {
        console.error('获取美食文化列表失败:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 加载美食文化详情
    async fetchFoodCultureById(id) {
      this.loading = true
      this.error = null
      
      try {
        this.selectedFoodCulture = await foodCultureApi.getFoodCultureById(id)
      } catch (error) {
        console.error(`获取美食文化详情失败 (ID: ${id}):`, error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 加载美食类型列表
    async fetchFoodTypes() {
      this.loading = true
      this.error = null
      
      try {
        this.foodTypes = await foodCultureApi.getFoodTypes()
      } catch (error) {
        console.error('获取美食类型列表失败:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 加载发源地区列表
    async fetchOriginDistricts() {
      this.loading = true
      this.error = null
      
      try {
        this.originDistricts = await foodCultureApi.getOriginDistricts()
      } catch (error) {
        console.error('获取发源地区列表失败:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 加载美食路线列表
    async fetchFoodRoutes(district = '') {
      this.loading = true
      this.error = null
      
      try {
        this.foodRoutes = await foodCultureApi.getFoodRoutes(district)
      } catch (error) {
        console.error('获取美食路线列表失败:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 加载美食路线详情
    async fetchFoodRouteById(id) {
      this.loading = true
      this.error = null
      
      try {
        this.selectedFoodRoute = await foodCultureApi.getFoodRouteById(id)
      } catch (error) {
        console.error(`获取美食路线详情失败 (ID: ${id}):`, error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 设置筛选条件
    setFilter(filterName, value) {
      this.filters[filterName] = value
    },
    
    // 重置筛选条件
    resetFilters() {
      this.filters = {
        foodType: '',
        district: ''
      }
    },
    
    // 清除选中的美食文化
    clearSelectedFoodCulture() {
      this.selectedFoodCulture = null
    },
    
    // 清除选中的美食路线
    clearSelectedFoodRoute() {
      this.selectedFoodRoute = null
    }
  }
}) 