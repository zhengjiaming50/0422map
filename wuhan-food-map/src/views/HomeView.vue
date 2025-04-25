<template>
  <div class="home">
    <header class="home-header cyber-border">
      <h1 class="glitch-effect neon-text">武汉美食地图</h1>
    </header>
    
    <main class="home-content">
      <div class="intro-card cyber-border">
        <h2 class="neon-text-pink">欢迎使用武汉美食地图系统</h2>
        <div class="actions">
          <router-link to="/map" class="cyber-btn">进入地图</router-link>
          <router-link to="/stats" class="cyber-btn cyber-btn-blue">查看统计</router-link>
          <router-link to="/food-culture" class="cyber-btn cyber-btn-yellow">美食文化</router-link>
        </div>
      </div>
    </main>

    <div class="cyber-lines"></div>
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
  position: relative;
  overflow: hidden;
}

.cyber-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  background-image: 
    linear-gradient(0deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: -1;
}

.home-header {
  margin-bottom: 2rem;
  padding: 2rem;
  background-color: rgba(26, 26, 26, 0.8);
}

h1 {
  font-size: 3.5rem;
  margin-bottom: 0.5rem;
  letter-spacing: 3px;
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
}

.subtitle {
  font-size: 1.5rem;
  color: var(--cp-cyan);
  font-weight: 300;
  letter-spacing: 2px;
}

.home-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

.intro-card {
  background-color: rgba(13, 13, 13, 0.85);
  padding: 2.5rem;
  max-width: 600px;
  position: relative;
}

.intro-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, var(--cp-cyan), transparent, var(--cp-pink));
  opacity: 0.05;
  z-index: -1;
}

.intro-card p {
  color: var(--cp-light);
  line-height: 1.6;
  margin: 1.5rem 0;
}

.actions {
  margin-top: 2.5rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
}

.cyber-btn {
  display: inline-block;
  padding: 0.8rem 2rem;
  text-decoration: none;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
  background-color: transparent;
  color: var(--cp-light);
  border: 2px solid var(--cp-cyan);
  box-shadow: 0 0 10px var(--cp-cyan), inset 0 0 10px var(--cp-cyan);
  transition: all 0.3s;
  overflow: hidden;
  font-family: 'Rajdhani', sans-serif;
}

.cyber-btn:hover {
  color: var(--cp-dark);
  background-color: var(--cp-cyan);
  text-shadow: none;
}

.cyber-btn-blue {
  border-color: var(--cp-blue);
  box-shadow: 0 0 10px var(--cp-blue), inset 0 0 10px var(--cp-blue);
}

.cyber-btn-blue:hover {
  background-color: var(--cp-blue);
}

.cyber-btn-yellow {
  border-color: var(--cp-yellow);
  box-shadow: 0 0 10px var(--cp-yellow), inset 0 0 10px var(--cp-yellow);
}

.cyber-btn-yellow:hover {
  background-color: var(--cp-yellow);
}

@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  .intro-card {
    padding: 1.5rem;
  }
  
  .actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .cyber-btn {
    width: 100%;
  }
}
</style> 