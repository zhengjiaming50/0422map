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
  }
} 