<template>
  <div class="home">
    <header class="home-header">
      <h1>武汉美食地图</h1>
      <p class="subtitle">探索武汉特色美食，发现城市美食文化</p>
    </header>
    
    <main class="home-content">
      <div class="intro-card">
        <h2>欢迎使用武汉美食地图系统</h2>
        <p>这里汇集了武汉各区域的特色餐厅和美食，点击下方按钮开始你的美食探索之旅。</p>
        <div class="actions">
          <router-link to="/map" class="map-btn">进入地图</router-link>
          <router-link to="/stats" class="stats-btn">查看统计</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// 组件逻辑可在这里添加
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.home-header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #d32f2f;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.home-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.intro-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
}

.actions {
  margin-top: 2rem;
}

.map-btn {
  display: inline-block;
  background-color: #d32f2f;
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
  margin: 0 0.5rem;
}

.map-btn:hover {
  background-color: #b71c1c;
}

.stats-btn {
  display: inline-block;
  background-color: #1976d2;
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
  margin: 0 0.5rem;
}

.stats-btn:hover {
  background-color: #0d47a1;
}
</style> 