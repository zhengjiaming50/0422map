<template>
  <div class="food-culture-container">
    <header class="culture-header">
      <h1>武汉美食文化</h1>
      <p class="subtitle">千年江城的味蕾记忆</p>
    </header>

    <div class="culture-nav">
      <a href="#intro" class="nav-item">文化简介</a>
      <a href="#famous-food" class="nav-item">特色名菜</a>
      <a href="#food-streets" class="nav-item">美食街区</a>
      <router-link to="/food-route" class="nav-item special">一日美食路线</router-link>
    </div>

    <section id="intro" class="culture-section">
      <h2>武汉美食文化简介</h2>
      <div class="culture-content">
        <img src="https://p1-q.mafengwo.net/s12/M00/5D/D7/wKgED1urUEyACSHYAAHXV0ZK9SU72.jpeg" alt="武汉美食总览" class="culture-image" />
        <div class="culture-text">
          <p>武汉，这座有着3500多年历史的江城，是长江中游地区的核心城市，也是中华饮食文化的重要代表城市之一。武汉美食融合了楚菜的精华，同时吸收了全国各地的烹饪技术，形成了独特的"江湖风味"。</p>
          <p>武汉美食以其"早点文化"闻名全国，从热干面到豆皮、鸭脖，再到各式小吃，每一道都承载着这座城市的历史与温度。武汉人喜欢吃早点的习惯可追溯到民国时期，如今已成为城市文化的重要标识。</p>
          <p>这里的美食特点可概括为：口味偏重、注重调味、鲜香麻辣、汤鲜料足。无论是街边小吃还是名店佳肴，都能体现出武汉人爽朗直率的性格特点。</p>
        </div>
      </div>
    </section>

    <section id="famous-food" class="culture-section">
      <h2>武汉特色名菜</h2>
      
      <div class="food-card">
        <img src="https://pic3.zhimg.com/80/v2-afb73698ea7c1e5b828ec1a06c85e913_720w.jpg" alt="热干面" class="food-image" />
        <div class="food-info">
          <h3>热干面</h3>
          <div class="food-tags">
            <span class="tag">早餐</span>
            <span class="tag">面食</span>
            <span class="tag">武汉名片</span>
          </div>
          <p class="food-desc">热干面是武汉最具代表性的传统名小吃，为中国十大面条之一。热干面源于19世纪末的武汉汉口，由一位叫李包的挑夫发明。其特点是先煮熟面条，再过冷水，拌以芝麻酱、香油、酱油、辣椒油等调料。吃正宗的热干面，"干而不硬，滑而不粘，香而不腻，辣而不燥"。</p>
          <p class="food-culture">热干面不仅是一种美食，更是武汉人记忆中不可或缺的一部分。无论身在何方，一碗热干面能勾起游子对家乡的思念；而对于武汉人来说，早上一碗热干面，才算真正开始了一天。</p>
        </div>
      </div>

      <div class="food-card reverse">
        <img src="https://youimg1.c-ctrip.com/target/100h0y000000m1mb0D9D3.jpg" alt="豆皮" class="food-image" />
        <div class="food-info">
          <h3>豆皮</h3>
          <div class="food-tags">
            <span class="tag">早餐</span>
            <span class="tag">小吃</span>
            <span class="tag">传统美食</span>
          </div>
          <p class="food-desc">武汉豆皮，是武汉著名的传统小吃之一。以糯米、米酒、蛋黄为底料，辅以香菇、虾仁等配料，裹以豆皮，上笼蒸熟，食时切块，浇以调味汁，色泽金黄，清香软糯，是武汉人早餐的首选之一。</p>
          <p class="food-culture">豆皮起源于清末民初时期的汉口，至今已有百年历史。传统的豆皮制作讲究选料、和馅、包制、蒸制等多道工序。武汉人常说"早上一碗热干面，一张豆皮垫底"，表达了对这一美食的热爱。</p>
        </div>
      </div>

      <div class="food-card">
        <img src="https://youimg1.c-ctrip.com/target/100k0z000000nunaaE86B.jpg" alt="鸭脖" class="food-image" />
        <div class="food-info">
          <h3>武汉鸭脖</h3>
          <div class="food-tags">
            <span class="tag">小吃</span>
            <span class="tag">卤味</span>
            <span class="tag">辣味</span>
          </div>
          <p class="food-desc">武汉鸭脖是以鸭脖为主要原料，配以多种香辛料和调味品，经过特殊工艺腌制、煮制、烘制而成的风味小吃。其特点是色泽红亮，肉质鲜嫩，香辣适口，回味悠长。</p>
          <p class="food-culture">武汉鸭脖兴起于上世纪80年代末，最初是由武汉街头小贩创制的。如今，它已成为全国知名的休闲食品，代表了武汉人对美食的创造力和对香辣味道的追求。人们喜欢边看电视边吃鸭脖，被称为"追剧神器"。</p>
        </div>
      </div>
    </section>

    <section id="food-streets" class="culture-section">
      <h2>武汉美食街区</h2>
      
      <div class="street-card">
        <h3>户部巷</h3>
        <p class="street-desc">位于武汉市武昌区解放路，是武汉著名的传统小吃一条街，汇集了热干面、豆皮、面窝、糊汤粉等几十种武汉特色小吃。这里店铺林立，香气四溢，是体验地道武汉美食的首选地。</p>
      </div>
      
      <div class="street-card">
        <h3>司门口美食街</h3>
        <p class="street-desc">位于武昌区，是武汉最富盛名的美食街之一。这里既有老字号名店，也有创新小吃，代表了武汉美食的传统与发展。特别是夜晚，灯火通明，人流如织，充满了烟火气息。</p>
      </div>
      
      <div class="street-card">
        <h3>吉庆街</h3>
        <p class="street-desc">位于汉口区，是一条具有百年历史的老街，以其丰富的江湖菜和地方小吃著称。这里的招牌菜有毛血旺、藕夹、豆皮等，保留了最原汁原味的武汉风味。</p>
      </div>
    </section>

    <div class="route-promo">
      <h2>想要体验一日武汉美食之旅？</h2>
      <p>我们精心设计了多条美食路线，帮助您一天内品尝武汉最具代表性的美食！</p>
      <router-link to="/food-route" class="promo-btn">查看美食路线</router-link>
    </div>
  </div>
</template>

<script setup>
// 可以在这里添加一些必要的逻辑，但根据需求，我们主要保持静态内容
</script>

<style scoped>
.food-culture-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  min-height: 100vh;
}

.culture-header {
  text-align: center;
  padding: 30px 0;
  background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
              url('https://youimg1.c-ctrip.com/target/100j1f000001gqb2iE27D.jpg') center/cover no-repeat;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
}

.culture-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  font-weight: 300;
}

.culture-nav {
  display: flex;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 15px 0;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.nav-item {
  margin: 0 15px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 8px 15px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: #e0e0e0;
}

.nav-item.special {
  background-color: #ff4d4f;
  color: white;
}

.nav-item.special:hover {
  background-color: #ff7875;
}

.culture-section {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.culture-section h2 {
  color: #333;
  padding-bottom: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid #ff4d4f;
}

.culture-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (min-width: 768px) {
  .culture-content {
    flex-direction: row;
  }
}

.culture-image {
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  object-fit: cover;
}

.culture-text {
  flex: 1;
}

.culture-text p {
  margin-bottom: 15px;
  line-height: 1.8;
}

.food-card {
  display: flex;
  flex-direction: column;
  margin-bottom: 30px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}

@media (min-width: 768px) {
  .food-card {
    flex-direction: row;
  }
  
  .food-card.reverse {
    flex-direction: row-reverse;
  }
}

.food-image {
  width: 100%;
  max-width: 300px;
  height: 250px;
  object-fit: cover;
}

.food-info {
  padding: 20px;
  flex: 1;
}

.food-info h3 {
  margin-bottom: 10px;
  color: #333;
  font-size: 1.5rem;
}

.food-tags {
  margin-bottom: 15px;
}

.tag {
  display: inline-block;
  background-color: #f5f5f5;
  color: #555;
  padding: 4px 8px;
  margin-right: 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.food-desc, .food-culture {
  margin-bottom: 15px;
  line-height: 1.7;
}

.food-culture {
  font-style: italic;
  color: #666;
}

.street-card {
  background-color: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.street-card h3 {
  color: #ff4d4f;
  margin-bottom: 10px;
}

.street-desc {
  line-height: 1.6;
}

.route-promo {
  background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
              url('https://youimg1.c-ctrip.com/target/100a1f000001grvzx2AB8.jpg') center/cover no-repeat;
  color: white;
  text-align: center;
  padding: 40px 20px;
  border-radius: 8px;
  margin-top: 40px;
}

.route-promo h2 {
  margin-bottom: 15px;
}

.route-promo p {
  margin-bottom: 20px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.promo-btn {
  display: inline-block;
  background-color: #ff4d4f;
  color: white;
  text-decoration: none;
  padding: 12px 25px;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.promo-btn:hover {
  background-color: #ff7875;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .culture-header h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .culture-nav {
    flex-wrap: wrap;
  }
  
  .nav-item {
    margin: 5px;
  }
}
</style> 