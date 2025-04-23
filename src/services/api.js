/**
 * 获取餐厅评价
 * @param {number} restaurantId - 餐厅ID
 * @returns {Promise<Array>} - 评价列表
 */
export const getRestaurantReviews = async (restaurantId) => {
  try {
    const response = await fetch(`/api/restaurants/${restaurantId}/reviews`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching restaurant reviews:', error);
    throw error;
  }
};

/**
 * 添加餐厅评价
 * @param {number} restaurantId - 餐厅ID
 * @param {Object} reviewData - 评价数据
 * @param {number} reviewData.rating - 评分(1-5)
 * @param {string} reviewData.comment - 评价内容
 * @param {string} reviewData.user_name - 用户名
 * @returns {Promise<Object>} - 新创建的评价
 */
export const addRestaurantReview = async (restaurantId, reviewData) => {
  try {
    const response = await fetch(`/api/restaurants/${restaurantId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(reviewData),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error adding restaurant review:', error);
    throw error;
  }
}; 