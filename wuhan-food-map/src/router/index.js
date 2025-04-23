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
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 