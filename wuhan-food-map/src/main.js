import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

// 创建应用实例
const app = createApp(App)

// 集成Pinia状态管理
app.use(createPinia())

// 集成Vue Router
app.use(router)

// 挂载应用
app.mount('#app')
