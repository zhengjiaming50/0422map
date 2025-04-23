import { createRouter, createWebHistory } from 'vue-router'

// 导入视图组件
import HomeView from '../views/HomeView.vue'

// 定义路由
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/map',
    name: 'map',
    // 懒加载地图视图，提高首页加载性能
    component: () => import('../views/MapView.vue')
  },
  {
    path: '/stats',
    name: 'stats',
    // 懒加载统计视图
    component: () => import('../views/StatsView.vue')
  },
  {
    path: '/food-culture',
    name: 'foodCulture',
    // 懒加载美食文化视图
    component: () => import('../views/FoodCultureView.vue')
  },
  {
    path: '/food-routes',
    name: 'foodRoutes',
    // 懒加载美食路线视图
    component: () => import('../views/FoodRouteView.vue')
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 