from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.models.food_culture import FoodCulture, FoodRoute, RouteStop
import datetime

# 武汉餐厅示例数据
sample_restaurants = [
    {
        'name': '黄鹤楼小吃店',
        'address': '武汉市武昌区蛇山西山坡特1号',
        'latitude': 30.5433,
        'longitude': 114.3008,
        'phone': '027-88888888',
        'food_type': '湖北菜',
        'description': '以热干面、豆皮等武汉特色小吃为主',
        'business_hours': '周一至周日 9:00-22:00',
        'district': '武昌区',
        'image_url': 'https://example.com/images/restaurant1.jpg'
    },
    {
        'name': '江汉路步行街小龙虾',
        'address': '武汉市江汉区江汉路步行街118号',
        'latitude': 30.5807,
        'longitude': 114.2986,
        'phone': '027-88889999',
        'food_type': '小吃',
        'description': '武汉特色麻辣小龙虾，肉质鲜嫩',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '江汉区',
        'image_url': 'https://example.com/images/restaurant2.jpg'
    },
    {
        'name': '户部巷老通城',
        'address': '武汉市武昌区解放路司门口户部巷20号',
        'latitude': 30.5527,
        'longitude': 114.3066,
        'phone': '027-88887777',
        'food_type': '糕点',
        'description': '百年老字号，传统汉式糕点',
        'business_hours': '周一至周日 8:00-20:00',
        'district': '武昌区',
        'image_url': 'https://example.com/images/restaurant3.jpg'
    },
    {
        'name': '楚河汉街烧烤',
        'address': '武汉市武昌区楚河汉街第8号楼附近',
        'latitude': 30.5564,
        'longitude': 114.3331,
        'phone': '027-88886666',
        'food_type': '烧烤',
        'description': '特色烤鱼，秘制调料',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '武昌区',
        'image_url': 'https://example.com/images/restaurant4.jpg'
    },
    {
        'name': '光谷步行街西餐厅',
        'address': '武汉市洪山区光谷步行街5号',
        'latitude': 30.5087,
        'longitude': 114.4182,
        'phone': '027-88885555',
        'food_type': '西餐',
        'description': '西式简餐，意面披萨',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '洪山区',
        'image_url': 'https://example.com/images/restaurant5.jpg'
    },
]

# 武汉特色美食文化数据
sample_food_cultures = [
    {
        'name': '热干面',
        'description': '热干面是武汉最负盛名的特色小吃，其特点是面条劲道、味道浓厚，配上芝麻酱、香油和生抽等调料，香气四溢。',
        'history': '热干面起源于民国初年，相传是由武汉汉口的一位摊贩偶然发明。最初是将剩余的汤面沥干，第二天加上调料卖给顾客，没想到生意异常火爆，由此发展成为武汉名小吃。',
        'making_method': '将新鲜面条煮熟后过凉水，沥干水分，拌入芝麻酱、香油、酱油、辣椒油和蒜末等调料，最后撒上葱花即可享用。',
        'food_type': '面食',
        'origin_district': '汉口',
        'image_url': 'https://example.com/images/hot_dry_noodles.jpg'
    },
    {
        'name': '豆皮',
        'description': '武汉豆皮是以绿豆等原料制成的薄皮，包裹糯米、木耳、蛋皮等食材，味道鲜美，外形似卷饼。',
        'history': '豆皮创始于清朝同治年间，最初由汉口粮道街的一家小店发明，现已成为江城武汉的著名小吃之一。',
        'making_method': '将绿豆磨成浆，摊成薄皮，包入糯米、木耳、蛋皮等配料，上锅蒸熟，切块食用。',
        'food_type': '小吃',
        'origin_district': '汉口',
        'image_url': 'https://example.com/images/doupi.jpg'
    },
    {
        'name': '武昌鱼',
        'description': '武昌鱼是长江中下游特有的鱼种，肉质鲜嫩，味道鲜美，是湖北武汉地区的特色菜肴。',
        'history': '武昌鱼在明朝时就极负盛名，据传明成祖朱棣曾品尝后赞不绝口，并特意赐名"武昌鱼"。',
        'making_method': '传统做法是清蒸，保持鱼的鲜美原味。先将鱼洗净，腌制入味，放入姜丝葱段，上锅清蒸，出锅后浇上热油提香。',
        'food_type': '湖北菜',
        'origin_district': '武昌',
        'image_url': 'https://example.com/images/wuchang_fish.jpg'
    },
    {
        'name': '小龙虾',
        'description': '武汉小龙虾以麻辣为主要口味，肉质鲜嫩，味道浓郁，是夏季夜宵的首选美食。',
        'history': '小龙虾原产于北美，20世纪70年代引入中国，在武汉地区因独特的烹饪方式迅速走红，形成了独特的小龙虾文化。',
        'making_method': '将小龙虾洗净，加入蒜、姜、辣椒等调料炒制，再加入啤酒、料酒炖煮，最后撒上香菜、花椒粉点缀。',
        'food_type': '湖北菜',
        'origin_district': '江汉区',
        'image_url': 'https://example.com/images/crayfish.jpg'
    },
    {
        'name': '三鲜豆皮',
        'description': '三鲜豆皮是武汉著名的传统名小吃，它以绿豆制成的薄皮，包裹着糯米、木耳、冬笋、鸡蛋、鲜肉等馅料，蒸制而成。',
        'history': '三鲜豆皮在清代就已经出现，最初在汉口地区流行，后来逐渐成为武汉三镇的著名小吃。',
        'making_method': '将绿豆磨浆滤出豆浆，制成豆皮，填入糯米、木耳、冬笋、蛋皮等馅料，上笼蒸熟，切块食用。',
        'food_type': '小吃',
        'origin_district': '江岸区',
        'image_url': 'https://example.com/images/sanxian_doupi.jpg'
    }
]

# 一日美食路线推荐数据
sample_food_routes = [
    {
        'name': '武汉经典小吃一日游',
        'description': '体验武汉最地道的传统小吃，包括热干面、豆皮、鲜鱼糊汤粉等经典美食。',
        'duration': '6小时',
        'district': '武昌区',
        'image_url': 'https://example.com/images/wuhan_food_tour.jpg'
    },
    {
        'name': '江滩夜宵美食之旅',
        'description': '傍晚开始的美食之旅，品尝武汉江滩附近的特色夜宵小吃，以小龙虾和烧烤为主。',
        'duration': '4小时',
        'district': '江汉区',
        'image_url': 'https://example.com/images/night_food_tour.jpg'
    },
    {
        'name': '老武汉早点探索',
        'description': '从早上开始，品尝武汉传统的早点，包括热干面、豆皮、糊汤粉、面窝等。',
        'duration': '3小时',
        'district': '汉阳区',
        'image_url': 'https://example.com/images/wuhan_breakfast.jpg'
    }
]

def seed_data():
    """填充测试数据"""
    app = create_app()
    with app.app_context():
        # 检查是否已有数据
        existing_count = Restaurant.query.count()
        
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 条餐厅记录，跳过数据填充")
            return
        
        # 添加示例餐厅数据
        for data in sample_restaurants:
            restaurant = Restaurant(
                name=data['name'],
                address=data['address'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                phone=data['phone'],
                food_type=data['food_type'],
                description=data['description'],
                business_hours=data['business_hours'],
                district=data['district'],
                image_url=data['image_url']
            )
            db.session.add(restaurant)
        
        # 提交事务
        db.session.commit()
        print(f"✅ 成功添加 {len(sample_restaurants)} 条餐厅记录")

def seed_reviews():
    """添加示例评价数据"""
    print("正在添加餐厅评价数据...")
    
    # 为第一个餐厅添加评价
    restaurant1 = Restaurant.query.first()
    if restaurant1:
        reviews1 = [
            Review(
                restaurant_id=restaurant1.id,
                rating=5,
                comment="这家餐厅的热干面真的非常好吃，面条劲道，调料香浓，强烈推荐！",
                user_name="美食家张三"
            ),
            Review(
                restaurant_id=restaurant1.id,
                rating=4,
                comment="环境不错，服务态度很好，就是价格稍微贵了点。",
                user_name="李四"
            ),
            Review(
                restaurant_id=restaurant1.id,
                rating=3,
                comment="一般般，没有特别惊艳的地方。",
                user_name="王五"
            )
        ]
        db.session.add_all(reviews1)
    
    # 为第二个餐厅添加评价
    restaurant2 = Restaurant.query.offset(1).first()
    if restaurant2:
        reviews2 = [
            Review(
                restaurant_id=restaurant2.id,
                rating=5,
                comment="这家店的菜品真的很地道，感觉回到了老家的味道，非常推荐！",
                user_name="赵六"
            ),
            Review(
                restaurant_id=restaurant2.id,
                rating=5,
                comment="服务员很热情，点了他们家的招牌菜，非常美味！",
                user_name="食客123"
            )
        ]
        db.session.add_all(reviews2)
    
    # 为其他餐厅添加随机评价
    restaurants = Restaurant.query.offset(2).all()
    for restaurant in restaurants:
        reviews = [
            Review(
                restaurant_id=restaurant.id,
                rating=4,
                comment="菜品种类丰富，味道不错，会再来的。",
                user_name="美食爱好者"
            ),
            Review(
                restaurant_id=restaurant.id,
                rating=3,
                comment="味道一般，但是服务很好。",
                user_name="匿名用户"
            )
        ]
        db.session.add_all(reviews)
    
    db.session.commit()
    print("✅ 餐厅评价数据添加完成。")

def seed_food_cultures():
    """添加美食文化数据"""
    print("正在添加美食文化数据...")
    
    # 检查是否已有数据
    existing_count = db.session.query(FoodCulture).count()
    if existing_count > 0:
        print(f"数据库中已有 {existing_count} 条美食文化记录，跳过数据填充")
        return
    
    # 添加美食文化数据
    for data in sample_food_cultures:
        food_culture = FoodCulture(
            name=data['name'],
            description=data['description'],
            history=data['history'],
            making_method=data['making_method'],
            food_type=data['food_type'],
            origin_district=data['origin_district'],
            image_url=data['image_url']
        )
        db.session.add(food_culture)
    
    db.session.commit()
    print(f"✅ 成功添加 {len(sample_food_cultures)} 条美食文化记录")
    
    # 关联美食与餐厅
    # 热干面关联到黄鹤楼小吃店
    hot_noodle = FoodCulture.query.filter_by(name="热干面").first()
    restaurant1 = Restaurant.query.filter_by(name="黄鹤楼小吃店").first()
    if hot_noodle and restaurant1:
        hot_noodle.restaurants.append(restaurant1)
    
    # 豆皮关联到户部巷老通城
    doupi = FoodCulture.query.filter_by(name="豆皮").first()
    restaurant3 = Restaurant.query.filter_by(name="户部巷老通城").first()
    if doupi and restaurant3:
        doupi.restaurants.append(restaurant3)
    
    # 小龙虾关联到江汉路步行街小龙虾
    crayfish = FoodCulture.query.filter_by(name="小龙虾").first()
    restaurant2 = Restaurant.query.filter_by(name="江汉路步行街小龙虾").first()
    if crayfish and restaurant2:
        crayfish.restaurants.append(restaurant2)
    
    db.session.commit()
    print("✅ 美食与餐厅关联完成")

def seed_food_routes():
    """添加美食路线数据"""
    print("正在添加美食路线数据...")
    
    # 检查是否已有数据
    existing_count = db.session.query(FoodRoute).count()
    if existing_count > 0:
        print(f"数据库中已有 {existing_count} 条美食路线记录，跳过数据填充")
        return
    
    # 添加美食路线数据
    for data in sample_food_routes:
        food_route = FoodRoute(
            name=data['name'],
            description=data['description'],
            duration=data['duration'],
            district=data['district'],
            image_url=data['image_url']
        )
        db.session.add(food_route)
    
    db.session.commit()
    print(f"✅ 成功添加 {len(sample_food_routes)} 条美食路线记录")
    
    # 添加路线站点
    # 武汉经典小吃一日游路线
    classic_route = FoodRoute.query.filter_by(name="武汉经典小吃一日游").first()
    if classic_route:
        # 站点1: 黄鹤楼小吃店
        restaurant1 = Restaurant.query.filter_by(name="黄鹤楼小吃店").first()
        if restaurant1:
            stop1 = RouteStop(
                route_id=classic_route.id,
                restaurant_id=restaurant1.id,
                stop_order=1,
                visit_time="上午10:00-11:30",
                recommendation="推荐尝试热干面和鲜肉包"
            )
            db.session.add(stop1)
        
        # 站点2: 户部巷老通城
        restaurant3 = Restaurant.query.filter_by(name="户部巷老通城").first()
        if restaurant3:
            stop2 = RouteStop(
                route_id=classic_route.id,
                restaurant_id=restaurant3.id,
                stop_order=2,
                visit_time="中午12:00-13:30",
                recommendation="推荐尝试三鲜豆皮和糯米包油条"
            )
            db.session.add(stop2)
        
        # 站点3: 楚河汉街烧烤
        restaurant4 = Restaurant.query.filter_by(name="楚河汉街烧烤").first()
        if restaurant4:
            stop3 = RouteStop(
                route_id=classic_route.id,
                restaurant_id=restaurant4.id,
                stop_order=3,
                visit_time="下午15:00-16:30",
                recommendation="推荐尝试特色烤鱼和烤豆腐"
            )
            db.session.add(stop3)
    
    # 江滩夜宵美食之旅
    night_route = FoodRoute.query.filter_by(name="江滩夜宵美食之旅").first()
    if night_route:
        # 站点1: 江汉路步行街小龙虾
        restaurant2 = Restaurant.query.filter_by(name="江汉路步行街小龙虾").first()
        if restaurant2:
            stop1 = RouteStop(
                route_id=night_route.id,
                restaurant_id=restaurant2.id,
                stop_order=1,
                visit_time="晚上18:00-20:00",
                recommendation="推荐尝试蒜蓉小龙虾和十三香小龙虾"
            )
            db.session.add(stop1)
        
        # 站点2: 楚河汉街烧烤
        if restaurant4:
            stop2 = RouteStop(
                route_id=night_route.id,
                restaurant_id=restaurant4.id,
                stop_order=2,
                visit_time="晚上20:30-22:00",
                recommendation="推荐尝试烤鱼和各种串串"
            )
            db.session.add(stop2)
    
    db.session.commit()
    print("✅ 美食路线站点添加完成")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_data()
        seed_reviews()
        seed_food_cultures()
        seed_food_routes()
        print("所有示例数据已添加完成。") 