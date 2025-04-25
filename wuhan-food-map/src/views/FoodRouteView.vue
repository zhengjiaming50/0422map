<template>
  <div class="food-route-container">
    <header class="route-header">
      <h1>武汉一日美食路线</h1>
      <p class="subtitle">用一天时间，尽享江城美食精华</p>
    </header>
    
    <div class="back-link">
      <router-link to="/food-culture" class="back-btn">
        &larr; 返回美食文化页面
      </router-link>
    </div>

    <div class="route-intro">
      <p>我们精心设计了几条美食路线，让您在一天内体验最地道的武汉美食。每条路线都考虑了餐厅的地理位置、特色菜品和用餐高峰时间，确保您有最佳的品尝体验。</p>
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
    name: "经典武汉早点之旅",
    duration: "6小时",
    food_count: 8,
    locations: 5,
    description: "早上从最地道的热干面、豆皮开始，中午品尝正宗的武昌鱼，下午享用各式武汉小吃，体验地道的武汉早点文化。",
    stops: [
      {
        time: "08:00",
        name: "蔡林记",
        type: "早餐",
        address: "武汉市武昌区洪山区珞瑜路20号",
        description: "创建于1931年的老字号，以地道的热干面和豆皮著称，是体验武汉早点文化的必去之地。",
        recommended_dishes: ["热干面", "豆皮", "面窝"],
        tips: "早上8点前去可避开早高峰人流，建议点一碗热干面配一张豆皮，体验最经典的武汉早餐搭配。"
      },
      {
        time: "10:30",
        name: "户部巷",
        type: "小吃街",
        address: "武汉市武昌区解放路特1号",
        description: "武汉著名的小吃街，汇集了众多武汉特色小吃，是了解武汉饮食文化的窗口。",
        recommended_dishes: ["鸭脖子", "面窝", "糊汤粉", "小龙虾"],
        tips: "巷子不长但店铺众多，可以少量多尝，不要一次点太多。"
      },
      {
        time: "12:30",
        name: "老通城",
        type: "午餐",
        address: "武汉市武昌区解放路372号",
        description: "创立于1920年的百年老店，以糯米甜点和鸭脖闻名，是武汉人喜爱的传统小吃店。",
        recommended_dishes: ["三鲜豆皮", "糯米包油条", "鸭脖"],
        tips: "老通城的甜食偏甜，如果不喜欢太甜的口味可以提前告知。"
      },
      {
        time: "15:00",
        name: "简朴寨",
        type: "下午茶",
        address: "武汉市武昌区司门口解放路190号",
        description: "以农家菜和本土小吃为主的餐厅，环境古朴，菜品地道实惠。",
        recommended_dishes: ["藕夹", "热干面", "汤包"],
        tips: "他们家的藕夹非常有名，香脆可口，一定要尝试。"
      },
      {
        time: "18:00",
        name: "湖锦酒楼",
        type: "晚餐",
        address: "武汉市武昌区中南路7号",
        description: "正宗的湖北菜馆，以武昌鱼和莲藕系列菜品闻名，环境优雅，适合晚餐。",
        recommended_dishes: ["清蒸武昌鱼", "藕带炒肉", "毛血旺", "糍粑鱼"],
        tips: "武昌鱼需要提前预订，建议下午致电餐厅预留。"
      }
    ],
    tips: [
      "此路线以步行和公共交通为主，全程约7公里，可乘坐地铁2号线在中南路站和洪山广场站之间活动。",
      "武汉早点店通常7-9点最为拥挤，建议错峰前往。",
      "夏季游览请做好防暑准备，户部巷全是露天小店，中午阳光强烈。",
      "可使用武汉地铁APP规划交通路线，更加便捷。"
    ]
  },
  {
    name: "江滨美食探索之旅",
    duration: "8小时",
    food_count: 10,
    locations: 6,
    description: "沿着长江和汉江探索武汉两江交汇处的美食文化，品尝江鲜和地方特色菜，感受武汉独特的江河文化。",
    stops: [
      {
        time: "09:00",
        name: "谌记热干面",
        type: "早餐",
        address: "武汉市江岸区胜利街18号",
        description: "位于武汉最古老区域之一的早点店，以正宗的热干面、灌汤包和豆皮为特色。",
        recommended_dishes: ["热干面", "灌汤包", "豆浆"],
        tips: "他家的热干面偏辣，如果不能吃辣可以提前告知。"
      },
      {
        time: "11:00",
        name: "黄鹤楼公园",
        type: "景点",
        address: "武汉市武昌区蛇山西山坡特1号",
        description: "游览武汉地标景点，远眺长江美景，为接下来的美食之旅积攒食欲。",
        tips: "公园内有不少小吃摊，但价格偏高，建议在外面餐厅用餐。"
      },
      {
        time: "13:00",
        name: "湖北佬",
        type: "午餐",
        address: "武汉市武昌区解放路23号",
        description: "以江鲜和地方家常菜闻名的餐厅，菜品种类丰富，口味正宗。",
        recommended_dishes: ["江团鱼煲", "清蒸武昌鱼", "鱼香茄子"],
        tips: "点菜时可以咨询服务员当季新鲜江鲜，通常会有特价。"
      },
      {
        time: "16:00",
        name: "江滨公园",
        type: "景点",
        address: "武汉市汉口江滨路",
        description: "沿江散步，欣赏武汉长江大桥和两岸风光，消化午餐，准备品尝下一站美食。",
        tips: "傍晚时分江边风景最美，也是拍照的好时机。"
      },
      {
        time: "18:30",
        name: "吉庆街",
        type: "晚餐",
        address: "武汉市江汉区吉庆街",
        description: "武汉著名的美食街，有众多老字号餐厅，夜晚灯火通明，氛围热闹。",
        recommended_dishes: ["四季美汤包", "周黑鸭", "花样年华小龙虾"],
        tips: "晚上6点后开始热闹，很多店铺会排队，建议提前到达。"
      },
      {
        time: "20:30",
        name: "江汉路步行街",
        type: "夜宵",
        address: "武汉市江汉区江汉路",
        description: "武汉最繁华的商业街之一，晚上有众多地道小吃和甜品店，是夜宵的理想去处。",
        recommended_dishes: ["三色冰激凌", "豆皮馄饨", "热干面"],
        tips: "步行街的甜品店大多营业到深夜，是结束一天美食之旅的完美收尾。"
      }
    ],
    tips: [
      "此路线跨越长江两岸，建议使用地铁和轮渡结合的方式出行。",
      "可以在黄鹤楼乘坐轮渡到汉口，体验武汉独特的江上交通。",
      "行程较长，建议穿着舒适的鞋子，并携带充足的水。",
      "夏季请注意防晒，江边紫外线较强。"
    ]
  },
  {
    name: "网红美食打卡之旅",
    duration: "7小时",
    food_count: 9,
    locations: 5,
    description: "探访近年来在社交媒体上走红的武汉特色美食店铺，品尝传统与创新结合的武汉美食。",
    stops: [
      {
        time: "10:00",
        name: "老谦记热干面",
        type: "早午餐",
        address: "武汉市洪山区珞瑜路20号",
        description: "在抖音等平台爆红的热干面店，每天都有长队，以传统工艺制作的热干面和创新小吃闻名。",
        recommended_dishes: ["招牌热干面", "爆浆鸡蛋饼", "小龙虾豆皮"],
        tips: "早上10点左右人相对较少，建议这个时间段前往。"
      },
      {
        time: "12:30",
        name: "楚留香小龙虾",
        type: "午餐",
        address: "武汉市洪山区光谷广场步行街",
        description: "以创新口味小龙虾著称的网红店，店内装修时尚，是年轻人喜爱的打卡地。",
        recommended_dishes: ["十三香小龙虾", "蒜香小龙虾", "虾滑豆腐煲"],
        tips: "点小龙虾时可以选择不同辣度，服务员会提供一次性手套。"
      },
      {
        time: "15:00",
        name: "文和友小吃",
        type: "下午茶",
        address: "武汉市武昌区街道口阜华大厦1楼",
        description: "复古风网红小吃店，以怀旧装修和创新武汉小吃走红，经常有网红主播直播打卡。",
        recommended_dishes: ["铁板鱿鱼", "爆浆鸡蛋糕", "冰粉"],
        tips: "店内场景非常适合拍照，可以多带几套衣服来此打卡。"
      },
      {
        time: "17:30",
        name: "武汉天地",
        type: "休闲",
        address: "武汉市江岸区中山大道1515号",
        description: "武汉高端商业区，有许多网红咖啡店和甜品店，适合晚餐前小憩。",
        recommended_dishes: ["脏脏包", "喜茶", "奈雪的茶"],
        tips: "这里的甜品咖啡价格偏高，但环境优美，值得一坐。"
      },
      {
        time: "19:00",
        name: "花样年华",
        type: "晚餐",
        address: "武汉市武昌区中南路68号",
        description: "融合了传统与现代的创意湖北菜餐厅，环境精致，菜品美观，是社交媒体热门打卡地。",
        recommended_dishes: ["梅菜扣肉", "荷包豆皮", "糍粑鲜鱼"],
        tips: "晚餐时段需要提前预约，菜品分量适中，适合多人共享。"
      }
    ],
    tips: [
      "此路线主要集中在武昌区和洪山区，可以乘坐地铁2号线和4号线前往。",
      "网红店通常客流量大，建议避开饭点高峰期。",
      "记得带上充电宝和足够内存的手机，拍照发朋友圈必不可少。",
      "部分网红店可能需要排队等位，请耐心等待。"
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