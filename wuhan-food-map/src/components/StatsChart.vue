<!-- 统计图表组件 -->
<template>
  <div class="stats-chart-container">
    <div v-if="loading" class="loading-container">
      <p>正在加载数据...</p>
    </div>
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
    </div>
    <div v-else class="chart-container">
      <div class="chart-header">
        <h3>{{ title }}</h3>
        <div class="chart-controls" v-if="showControls">
          <select v-model="selectedFoodType" @change="updateChartData" class="food-type-select">
            <option value="">所有美食类型</option>
            <option v-for="type in foodTypeList" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
      </div>
      <Bar
        v-if="chartData"
        :data="chartData"
        :options="chartOptions"
        class="chart"
      />
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { computed, ref, onMounted } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'

// 注册Chart.js组件
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'StatsChart',
  components: {
    Bar
  },
  props: {
    title: {
      type: String,
      default: '武汉美食统计'
    },
    showControls: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const restaurantStore = useRestaurantStore()
    const loading = ref(false)
    const error = ref(null)
    const chartData = ref(null)
    const selectedFoodType = ref('')
    const foodTypeList = computed(() => restaurantStore.foodTypeList)
    
    // 图表配置
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
    
    // 加载图表数据
    const loadChartData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 确保有美食类型列表数据
        if (foodTypeList.value.length === 0) {
          await restaurantStore.fetchFoodTypeList()
        }
        
        // 获取统计数据
        await updateChartData()
      } catch (err) {
        error.value = '加载统计数据失败: ' + err.message
        console.error('加载统计数据失败:', err)
      } finally {
        loading.value = false
      }
    }
    
    // 更新图表数据
    const updateChartData = async () => {
      try {
        const statsData = await restaurantStore.fetchStatsByDistrictFoodType(selectedFoodType.value)
        
        if (!statsData || !statsData.categories || !statsData.series) {
          error.value = '统计数据格式错误'
          return
        }
        
        // 设置图表数据
        chartData.value = {
          labels: statsData.categories,
          datasets: statsData.series.map((series, index) => ({
            label: series.name,
            data: series.data,
            backgroundColor: getColor(index),
            borderColor: getDarkerColor(index),
            borderWidth: 1
          }))
        }
      } catch (err) {
        error.value = '更新图表数据失败: ' + err.message
        console.error('更新图表数据失败:', err)
      }
    }
    
    // 颜色生成函数
    const colors = [
      'rgba(255, 99, 132, 0.7)',
      'rgba(54, 162, 235, 0.7)',
      'rgba(255, 206, 86, 0.7)',
      'rgba(75, 192, 192, 0.7)',
      'rgba(153, 102, 255, 0.7)',
      'rgba(255, 159, 64, 0.7)',
      'rgba(199, 199, 199, 0.7)',
      'rgba(83, 102, 255, 0.7)',
      'rgba(40, 159, 150, 0.7)',
      'rgba(210, 105, 30, 0.7)'
    ]
    
    const getColor = (index) => {
      return colors[index % colors.length]
    }
    
    const getDarkerColor = (index) => {
      const color = colors[index % colors.length]
      return color.replace('0.7', '1.0')
    }
    
    // 组件挂载后加载数据
    onMounted(() => {
      loadChartData()
    })
    
    return {
      loading,
      error,
      chartData,
      chartOptions,
      selectedFoodType,
      foodTypeList,
      updateChartData
    }
  }
}
</script>

<style scoped>
.stats-chart-container {
  width: 100%;
  padding: 1rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.chart-controls {
  display: flex;
  gap: 1rem;
}

.food-type-select {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.chart-container {
  width: 100%;
  height: 400px;
}

.chart {
  width: 100%;
  height: 100%;
}

.loading-container,
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  color: #666;
}

.error-container {
  color: #d32f2f;
}
</style> 