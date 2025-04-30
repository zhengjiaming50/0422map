<template>
  <div class="food-route-container">
    <header class="route-header">
      <h1>成都一日美食路线</h1>
      <p class="subtitle">用一天时间，尽享蓉城美食精华</p>
    </header>
    
    <div class="back-link">
      <router-link to="/food-culture" class="back-btn">
        &larr; 返回美食文化页面
      </router-link>
    </div>

    <div class="route-intro">
      <p>我们精心设计了几条美食路线，让您在一天内体验最地道的成都美食。每条路线都考虑了餐厅的地理位置、特色菜品和用餐高峰时间，确保您有最佳的品尝体验。</p>
    </div>

    <!-- 路线选择器 -->
    <div class="route-tabs">
      <div 
        v-for="(route, index) in routes" 
        :key="index"
        class="route-tab"
        :class="{ active: activeRoute === index }"
        @click="activeRoute = index"
      >
        {{ route.name }}
      </div>
    </div>

    <!-- 当前选中的路线详情 -->
    <div class="route-detail" v-if="routes[activeRoute]">
      <div class="route-heading">
        <h2>{{ routes[activeRoute].name }}</h2>
        <div class="route-info">
          <span class="info-item"><i class="time-icon">⏱️</i> {{ routes[activeRoute].duration }}</span>
          <span class="info-item"><i class="food-icon">🍜</i> {{ routes[activeRoute].food_count }}种美食</span>
          <span class="info-item"><i class="location-icon">📍</i> {{ routes[activeRoute].locations }}个地点</span>
        </div>
        <p class="route-desc">{{ routes[activeRoute].description }}</p>
      </div>

      <div class="route-timeline">
        <div 
          v-for="(stop, stopIndex) in routes[activeRoute].stops" 
          :key="stopIndex" 
          class="timeline-item"
        >
          <div class="time-point">
            <div class="time">{{ stop.time }}</div>
            <div class="point"></div>
          </div>
          <div class="stop-card">
            <div class="stop-header">
              <h3>{{ stop.name }}</h3>
              <span class="stop-type">{{ stop.type }}</span>
            </div>
            <div class="stop-content">
              <img v-if="stop.image" :src="stop.image" :alt="stop.name" class="stop-image">
              <div class="stop-details">
                <p class="stop-address"><i class="address-icon">📍</i> {{ stop.address }}</p>
                <p class="stop-desc">{{ stop.description }}</p>
                <div v-if="stop.recommended_dishes" class="dishes">
                  <h4>推荐菜品：</h4>
                  <ul class="dish-list">
                    <li v-for="(dish, dishIndex) in stop.recommended_dishes" :key="dishIndex">
                      {{ dish }}
                    </li>
                  </ul>
                </div>
                <div class="stop-tips" v-if="stop.tips">
                  <h4>小贴士：</h4>
                  <p>{{ stop.tips }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="route-tips">
        <h3>路线小贴士</h3>
        <ul>
          <li v-for="(tip, tipIndex) in routes[activeRoute].tips" :key="tipIndex">
            {{ tip }}
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';

// 设置当前活跃路线
const activeRoute = ref(0);

// 路线数据
const routes = ref([
  {
    name: "经典成都小吃之旅",
    duration: "6小时",
    food_count: 8,
    locations: 5,
    description: "早上从最地道的担担面、钵钵鸡开始，中午品尝正宗的火锅，下午享用各式成都小吃，体验地道的成都休闲美食文化。",
    stops: [
      {
        time: "08:00",
        name: "陈麻婆豆腐",
        type: "早餐",
        address: "成都市青羊区西御河沿街23号",
        description: "创建于1862年的老字号，以正宗麻婆豆腐著称，是体验成都传统美食的必去之地。",
        recommended_dishes: ["麻婆豆腐", "担担面", "夫妻肺片"],
        tips: "早上8点前去可避开早高峰人流，建议点一碗担担面配上麻婆豆腐，体验最经典的成都早餐搭配。"
      },
      {
        time: "10:30",
        name: "宽窄巷子",
        type: "小吃街",
        address: "成都市青羊区金河路口宽窄巷子",
        description: "成都著名的小吃街，汇集了众多成都特色小吃，是了解成都饮食文化的窗口。",
        recommended_dishes: ["三大炮", "钵钵鸡", "兔头", "糖油果子"],
        tips: "巷子不长但店铺众多，可以少量多尝，不要一次点太多。"
      },
      {
        time: "12:30",
        name: "蜀九香火锅",
        type: "午餐",
        address: "成都市锦江区春熙路99号",
        description: "成都知名火锅品牌，以正宗川味火锅和新鲜食材著称，是体验成都火锅文化的绝佳去处。",
        recommended_dishes: ["鸳鸯锅底", "毛肚", "黄喉", "鲜牛肉"],
        tips: "火锅偏辣，如果不能吃辣可以选择鸳鸯锅，清汤区域不辣。"
      },
      {
        time: "15:00",
        name: "甜水面馆",
        type: "下午茶",
        address: "成都市武侯区锦里古街45号",
        description: "以传统川菜和本土小吃为主的餐厅，环境古朴，菜品地道实惠。",
        recommended_dishes: ["甜水面", "红油抄手", "凉糕"],
        tips: "他们家的甜水面非常有名，香甜可口，一定要尝试。"
      },
      {
        time: "18:00",
        name: "成都印象",
        type: "晚餐",
        address: "成都市武侯区科华北路65号",
        description: "正宗的四川菜馆，以回锅肉和鱼香系列菜品闻名，环境优雅，适合晚餐。",
        recommended_dishes: ["回锅肉", "水煮鱼", "鱼香肉丝", "夫妻肺片"],
        tips: "部分招牌菜需要提前预订，建议下午致电餐厅预留。"
      }
    ],
    tips: [
      "此路线以步行和公共交通为主，全程约7公里，可乘坐地铁1号线在春熙路站和天府广场站之间活动。",
      "成都小吃店通常9-11点最为拥挤，建议错峰前往。",
      "夏季游览请做好防暑准备，宽窄巷子部分店铺是露天的，中午阳光强烈。",
      "可使用成都地铁APP规划交通路线，更加便捷。"
    ]
  },
  {
    name: "锦江美食探索之旅",
    duration: "8小时",
    food_count: 10,
    locations: 6,
    description: "沿着锦江探索成都市中心的美食文化，品尝川菜和地方特色小吃，感受成都独特的休闲文化。",
    stops: [
      {
        time: "09:00",
        name: "赖汤圆",
        type: "早餐",
        address: "成都市锦江区春熙路南段18号",
        description: "位于成都最繁华商圈的传统小吃店，以香甜可口的汤圆和担担面为特色。",
        recommended_dishes: ["担担面", "甜汤圆", "豆浆"],
        tips: "他家的担担面偏辣，如果不能吃辣可以提前告知。"
      },
      {
        time: "11:00",
        name: "杜甫草堂",
        type: "景点",
        address: "成都市青羊区青华路37号",
        description: "游览成都地标景点，感受历史文化氛围，为接下来的美食之旅积攒食欲。",
        tips: "景点周边有不少小吃摊，但价格偏高，建议在外面餐厅用餐。"
      },
      {
        time: "13:00",
        name: "川西坝子",
        type: "午餐",
        address: "成都市武侯区科华北路23号",
        description: "以正宗川菜和地方家常菜闻名的餐厅，菜品种类丰富，口味地道。",
        recommended_dishes: ["水煮牛肉", "麻婆豆腐", "回锅肉"],
        tips: "点菜时可以咨询服务员当季特色菜品，通常会有推荐。"
      },
      {
        time: "16:00",
        name: "锦江公园",
        type: "景点",
        address: "成都市锦江区滨江路",
        description: "沿江散步，欣赏成都锦江风光，消化午餐，准备品尝下一站美食。",
        tips: "公园内有茶馆，可以小憩片刻，品尝地道的成都盖碗茶。"
      }
    ],
    tips: [
      "此路线涵盖成都市中心区域，建议使用公共交通，避开交通高峰期。",
      "成都的茶馆文化非常丰富，建议留出时间在某个茶馆小坐，感受当地生活。",
      "尝试小吃时注意辣度，成都的辣味通常比较重，可以提前告知店家调整。"
    ]
  }
]);
</script>

<style scoped>
.food-route-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  min-height: 100vh;
  height: 100%;
  overflow-y: auto;
  position: relative;
}

.route-header {
  text-align: center;
  padding: 30px 0;
  background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
              url('/img/route-header-bg.jpg') center/cover no-repeat;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
}

.route-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  font-weight: 300;
}

.back-link {
  margin-bottom: 20px;
}

.back-btn {
  display: inline-block;
  text-decoration: none;
  color: #555;
  padding: 8px 15px;
  border-radius: 4px;
  background-color: #f5f5f5;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #e0e0e0;
}

.route-intro {
  margin-bottom: 30px;
  line-height: 1.7;
  padding: 0 20px;
}

.route-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
  padding: 0 20px;
}

.route-tab {
  padding: 12px 20px;
  background-color: #f5f5f5;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  font-weight: 500;
}

.route-tab.active {
  background-color: #ff4d4f;
  color: white;
}

.route-tab:hover:not(.active) {
  background-color: #e0e0e0;
}

.route-detail {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.route-heading {
  margin-bottom: 30px;
  border-bottom: 2px solid #ff4d4f;
  padding-bottom: 20px;
}

.route-heading h2 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #333;
}

.route-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  color: #666;
}

.info-item i {
  margin-right: 5px;
}

.route-desc {
  line-height: 1.7;
  color: #555;
}

.route-timeline {
  position: relative;
}

.route-timeline::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 80px;
  width: 2px;
  background-color: #ff4d4f;
}

.timeline-item {
  display: flex;
  margin-bottom: 30px;
  position: relative;
}

.time-point {
  width: 80px;
  text-align: right;
  padding-right: 20px;
  position: relative;
  flex-shrink: 0;
}

.time {
  font-weight: 500;
  color: #555;
}

.point {
  position: absolute;
  right: -6px;
  top: 0;
  width: 12px;
  height: 12px;
  background-color: #ff4d4f;
  border-radius: 50%;
  z-index: 1;
}

.stop-card {
  flex: 1;
  margin-left: 20px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

.stop-header {
  padding: 15px 20px;
  background-color: #f5f5f5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stop-header h3 {
  margin: 0;
  color: #333;
}

.stop-type {
  background-color: #ff4d4f;
  color: white;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
}

.stop-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .stop-content {
    flex-direction: row;
    gap: 20px;
  }
}

.stop-image {
  width: 100%;
  max-width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 15px;
}

@media (min-width: 768px) {
  .stop-image {
    margin-bottom: 0;
  }
}

.stop-details {
  flex: 1;
}

.stop-address {
  color: #666;
  margin-bottom: 15px;
  display: flex;
  align-items: flex-start;
}

.address-icon {
  margin-right: 5px;
  display: inline-block;
}

.stop-desc {
  line-height: 1.7;
  margin-bottom: 15px;
}

.dishes h4, .stop-tips h4 {
  margin-bottom: 10px;
  font-weight: 500;
  color: #333;
}

.dish-list {
  padding-left: 20px;
}

.dish-list li {
  margin-bottom: 5px;
}

.stop-tips {
  margin-top: 15px;
  padding: 15px;
  background-color: #fff9f9;
  border-radius: 8px;
  border-left: 3px solid #ff4d4f;
}

.route-tips {
  margin-top: 30px;
  padding: 20px;
  background-color: #fff9f9;
  border-radius: 8px;
  border: 1px dashed #ff4d4f;
}

.route-tips h3 {
  margin-bottom: 15px;
  color: #333;
}

.route-tips ul {
  padding-left: 20px;
}

.route-tips li {
  margin-bottom: 10px;
  line-height: 1.7;
}

.route-map {
  margin-top: 40px;
  text-align: center;
  padding: 30px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.route-map h3 {
  margin-bottom: 20px;
  color: #333;
}

.map-placeholder {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.map-image {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
  border-radius: 8px;
}

.map-btn {
  display: inline-block;
  background-color: #ff4d4f;
  color: white;
  text-decoration: none;
  padding: 12px 25px;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.map-btn:hover {
  background-color: #ff7875;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .route-header h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .route-detail {
    padding: 15px;
  }
  
  .route-timeline::before {
    left: 50px;
  }
  
  .time-point {
    width: 50px;
  }
  
  .route-tabs {
    justify-content: center;
  }
  
  .route-tab {
    flex: 1;
    min-width: 120px;
  }
}
</style> 