// 添加评价相关的状态和方法

// ... existing code ...

// 在状态部分添加
/**
 * reviewsByRestaurantId: Map<number, Array> - 按餐厅ID存储的评价
 * reviewsLoading: boolean - 评价加载状态
 * reviewsError: string - 评价加载错误信息
 */

// 在actions部分添加
/**
 * 获取指定餐厅的评价
 * @param {number} restaurantId - 餐厅ID
 */
async function fetchRestaurantReviews(restaurantId) {
  if (!restaurantId) return;
  
  reviewsLoading.value = true;
  reviewsError.value = null;
  
  try {
    const reviews = await api.getRestaurantReviews(restaurantId);
    // 使用Map存储每个餐厅的评价，确保不同餐厅显示不同评价
    if (!reviewsByRestaurantId.value) {
      reviewsByRestaurantId.value = new Map();
    }
    reviewsByRestaurantId.value.set(restaurantId, reviews);
  } catch (err) {
    console.error(`Failed to fetch reviews for restaurant ${restaurantId}:`, err);
    reviewsError.value = '无法加载评价数据';
  } finally {
    reviewsLoading.value = false;
  }
}

/**
 * 提交新评价
 * @param {number} restaurantId - 餐厅ID
 * @param {Object} reviewData - 评价数据
 */
async function addReview(restaurantId, reviewData) {
  try {
    const newReview = await api.addRestaurantReview(restaurantId, reviewData);
    
    // 如果已经加载了这个餐厅的评价，更新缓存
    if (reviewsByRestaurantId.value && reviewsByRestaurantId.value.has(restaurantId)) {
      const currentReviews = reviewsByRestaurantId.value.get(restaurantId) || [];
      reviewsByRestaurantId.value.set(restaurantId, [newReview, ...currentReviews]);
    }
    
    return newReview;
  } catch (err) {
    console.error(`Failed to add review for restaurant ${restaurantId}:`, err);
    throw err;
  }
}

// ... existing code ... 