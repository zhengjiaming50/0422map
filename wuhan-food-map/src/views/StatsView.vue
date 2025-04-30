<!-- 统计页面 -->
<template>
  <div class="stats-view">
    <div class="header">
      <h1>成都美食统计</h1>
      <div class="nav-links">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/map" class="nav-link">地图</router-link>
      </div>
    </div>
    
    <div class="stats-container">
      <div class="chart-card">
        <h2>各区域美食类型分布</h2>
        <div class="chart-description">
          <p>此图表展示了成都各区域不同美食类型的餐厅数量分布。您可以通过下拉菜单选择特定美食类型查看其在各区域的分布情况。</p>
        </div>
        <StatsChart
          title="各区域美食类型分布统计"
          :showControls="true"
          class="district-food-chart"
        />
      </div>
    </div>
  </div>
</template>

<script>
import StatsChart from '../components/StatsChart.vue'

export default {
  name: 'StatsView',
  components: {
    StatsChart
  }
}
</script>

<style scoped>
.stats-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0;
  color: #333;
  font-size: 1.8rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: #1976d2;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(25, 118, 210, 0.1);
}

.stats-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.chart-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.chart-card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.4rem;
}

.chart-description {
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.95rem;
}

.district-food-chart {
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .stats-view {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style> 