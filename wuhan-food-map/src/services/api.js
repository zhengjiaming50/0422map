// API服务模块，处理与后端的所有HTTP请求

// API基础URL，实际开发中会配置到环境变量中
const API_BASE_URL = 'http://localhost:5000/api'

// 餐厅API服务
export const restaurantApi = {
  // 获取餐厅列表，可接受筛选条件
  async getRestaurants(filters = {}) {
    try {
      const queryParams = new URLSearchParams()
      
      // 添加筛选参数
      if (filters.district) queryParams.append('district', filters.district)
      if (filters.foodType) queryParams.append('food_type', filters.foodType)
      if (filters.query) queryParams.append('query', filters.query)
      
      const url = `${API_BASE_URL}/restaurants/?${queryParams.toString()}`
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取餐厅列表失败:', error)
      throw error
    }
  },
  
  // 获取指定ID的餐厅详情
  async getRestaurantById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${id}`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`获取餐厅详情失败 (ID: ${id}):`, error)
      throw error
    }
  },
  
  // 获取所有区域列表
  async getDistricts() {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/districts`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取区域列表失败:', error)
      throw error
    }
  },
  
  // 获取所有美食类型列表
  async getFoodTypes() {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/food-types`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取美食类型列表失败:', error)
      throw error
    }
  },
  
  // 获取指定边界框内的餐厅列表
  async getRestaurantsInBoundingBox(bounds) {
    try {
      const { minLng, minLat, maxLng, maxLat } = bounds
      const queryParams = new URLSearchParams({
        min_lng: minLng,
        min_lat: minLat,
        max_lng: maxLng,
        max_lat: maxLat
      })
      
      const url = `${API_BASE_URL}/restaurants/bbox?${queryParams.toString()}`
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取边界框内餐厅失败:', error)
      throw error
    }
  },
  
  // 获取指定餐厅的评价列表
  async getRestaurantReviews(restaurantId) {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}/reviews`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`获取餐厅评价失败 (ID: ${restaurantId}):`, error)
      throw error
    }
  },
  
  // 提交餐厅评价
  async submitReview(restaurantId, reviewData) {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/${restaurantId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || `API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`提交餐厅评价失败 (ID: ${restaurantId}):`, error)
      throw error
    }
  },
  
  // 获取热力图数据
  async getHeatmapData() {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/heatmap-data`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取热力图数据失败:', error)
      throw error
    }
  },
  
  // 获取按区域统计的餐厅数量
  async getStatsByDistrict() {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/stats/by-district`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取区域统计数据失败:', error)
      throw error
    }
  },
  
  // 获取按美食类型统计的餐厅数量
  async getStatsByFoodType() {
    try {
      const response = await fetch(`${API_BASE_URL}/restaurants/stats/by-food-type`)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取美食类型统计数据失败:', error)
      throw error
    }
  },
  
  // 获取按区域和美食类型交叉统计的餐厅数量
  async getStatsByDistrictFoodType(foodType = '') {
    try {
      let url = `${API_BASE_URL}/restaurants/stats/by-district-food-type`
      
      // 如果提供了特定美食类型，则添加到查询参数
      if (foodType) {
        const queryParams = new URLSearchParams({ food_type: foodType })
        url = `${url}?${queryParams.toString()}`
      }
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取区域美食类型交叉统计数据失败:', error)
      throw error
    }
  }
} 

// 路线规划API服务
export const routeApi = {
  // 获取路线规划
  async getRoute(routeParams) {
    try {
      const { start, end, mode } = routeParams
      
      const queryParams = new URLSearchParams({
        start_lng: start.lng,
        start_lat: start.lat,
        end_lng: end.lng,
        end_lat: end.lat,
        mode: mode || 'walking'
      })
      
      const url = `${API_BASE_URL}/routes/?${queryParams.toString()}`
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`API错误: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('获取路线规划失败:', error)
      throw error
    }
  }
} 