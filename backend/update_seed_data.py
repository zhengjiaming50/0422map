from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.review import Review
import random
from sqlalchemy import text

# 武汉餐厅示例数据 (增加到20个，并更新image_url)
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
        'image_url': '/images/restaurants/restaurant_1.jpg' # 热干面
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
        'image_url': '/images/restaurants/restaurant_2.jpg' # 麻辣小龙虾
    },
    {
        'name': '户部巷老通城',
        'address': '武汉市武昌区解放路司门口户部巷20号',
        'latitude': 30.5527,
        'longitude': 114.3066,
        'phone': '027-88887777',
        'food_type': '糕点',
        'description': '百年老字号，专营三鲜豆皮',
        'business_hours': '周一至周日 8:00-20:00',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_3.jpg' # 三鲜豆皮
    },
    {
        'name': '楚河汉街烧烤',
        'address': '武汉市武昌区楚河汉街第8号楼附近',
        'latitude': 30.5564,
        'longitude': 114.3331,
        'phone': '027-88886666',
        'food_type': '烧烤',
        'description': '特色烤鱼，秘制调料，外焦里嫩',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_4.jpg' # 烤鱼
    },
    {
        'name': '光谷步行街西餐厅',
        'address': '武汉市洪山区光谷步行街5号',
        'latitude': 30.5087,
        'longitude': 114.4182,
        'phone': '027-88885555',
        'food_type': '西餐',
        'description': '西式简餐，特色牛排和意面',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '洪山区',
        'image_url': '/images/restaurants/restaurant_5.jpg' # 牛排
    },
    {
        'name': '老字号蔡林记',
        'address': '武汉市江汉区民生路88号',
        'latitude': 30.5775,
        'longitude': 114.2930,
        'phone': '027-88881111',
        'food_type': '湖北菜',
        'description': '经典黑芝麻酱热干面，武汉必吃',
        'business_hours': '周一至周日 6:00-21:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_6.jpg' # 蔡林记热干面
    },
    {
        'name': '四季美汤包馆',
        'address': '武汉市江汉区中山大道668号',
        'latitude': 30.5758,
        'longitude': 114.2885,
        'phone': '027-88882222',
        'food_type': '小吃',
        'description': '皮薄馅足，汤汁鲜美的汤包',
        'business_hours': '周一至周日 7:00-20:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_7.jpg' # 汤包
    },
    {
        'name': '武昌鱼馆总店',
        'address': '武汉市武昌区彭刘杨路232号',
        'latitude': 30.5401,
        'longitude': 114.3052,
        'phone': '027-88876543',
        'food_type': '湖北菜',
        'description': '正宗清蒸武昌鱼，肉质细嫩鲜美',
        'business_hours': '周一至周日 10:00-21:30',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_8.jpg' # 清蒸武昌鱼
    },
    {
        'name': '汉口精武鸭脖',
        'address': '武汉市江汉区精武路1号',
        'latitude': 30.5691,
        'longitude': 114.2788,
        'phone': '027-88883333',
        'food_type': '小吃',
        'description': '麻辣鲜香的鸭脖，武汉特产',
        'business_hours': '周一至周日 10:00-23:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_9.jpg' # 鸭脖
    },
    {
        'name': '粮道街油饼包烧麦',
        'address': '武汉市武昌区粮道街文华中学旁',
        'latitude': 30.5480,
        'longitude': 114.3105,
        'phone': '无',
        'food_type': '小吃',
        'description': '油饼包裹着糯米烧麦，独特口感',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_10.jpg' # 油饼包烧麦
    },
    {
        'name': '徐嫂糊汤粉',
        'address': '武汉市武昌区自由路户部巷内',
        'latitude': 30.5525,
        'longitude': 114.3068,
        'phone': '无',
        'food_type': '小吃',
        'description': '鲜鱼熬制的糊汤搭配细粉，配油条更佳',
        'business_hours': '周一至周日 6:00-13:00',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_11.jpg' # 糊汤粉
    },
    {
        'name': '东湖排骨藕汤',
        'address': '武汉市洪山区东湖风景区听涛景区旁',
        'latitude': 30.5610,
        'longitude': 114.3680,
        'phone': '027-88884444',
        'food_type': '湖北菜',
        'description': '粉糯的洪湖藕与排骨慢炖，汤鲜味美',
        'business_hours': '周一至周日 10:30-21:00',
        'district': '洪山区',
        'image_url': '/images/restaurants/restaurant_12.jpg' # 排骨藕汤
    },
    {
        'name': '亢龙太子酒轩(临江总店)',
        'address': '武汉市江岸区沿江大道182号',
        'latitude': 30.5888,
        'longitude': 114.3121,
        'phone': '027-82788888',
        'food_type': '粤菜',
        'description': '高档粤菜餐厅，适合商务宴请',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '江岸区',
        'image_url': '/images/restaurants/restaurant_13.jpg' # 精致粤菜点心
    },
    {
        'name': '巴厘龙虾(万松园总店)',
        'address': '武汉市江汉区万松园路100号',
        'latitude': 30.5850,
        'longitude': 114.2785,
        'phone': '027-85777779',
        'food_type': '小吃',
        'description': '油焖大虾是招牌，口味多样',
        'business_hours': '周一至周日 16:00-03:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_14.jpg' # 油焖大虾
    },
    {
        'name': '靓靓蒸虾(雪松路总店)',
        'address': '武汉市江汉区雪松路69号',
        'latitude': 30.5845,
        'longitude': 114.2778,
        'phone': '027-85757757',
        'food_type': '小吃',
        'description': '清蒸小龙虾，原汁原味，蘸料独特',
        'business_hours': '周一至周日 11:00-02:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_15.jpg' # 清蒸小龙虾
    },
    {
        'name': '老街烧烤(万达店)',
        'address': '武汉市武昌区水果湖步行街万达广场旁',
        'latitude': 30.5550,
        'longitude': 114.3400,
        'phone': '027-87339999',
        'food_type': '烧烤',
        'description': '种类丰富的烧烤，烤鸡爪、烤茄子受欢迎',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '武昌区',
        'image_url': '/images/restaurants/restaurant_16.jpg' # 烤鸡爪
    },
    {
        'name': '严氏烧麦(自治街店)',
        'address': '武汉市江汉区自治街240号',
        'latitude': 30.5795,
        'longitude': 114.2830,
        'phone': '无',
        'food_type': '小吃',
        'description': '重油烧麦，胡椒味浓郁，糯米软糯',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_17.jpg' # 重油烧麦
    },
    {
        'name': '德华楼(汉口总店)',
        'address': '武汉市江汉区中山大道833号',
        'latitude': 30.5740,
        'longitude': 114.2875,
        'phone': '027-82836840',
        'food_type': '小吃',
        'description': '包子、年糕、水饺等传统汉味小吃',
        'business_hours': '周一至周日 7:00-20:00',
        'district': '江汉区',
        'image_url': '/images/restaurants/restaurant_18.jpg' # 德华楼包子
    },
    {
        'name': '田师傅热干面(山海关路店)',
        'address': '武汉市江岸区山海关路12号',
        'latitude': 30.5932,
        'longitude': 114.3158,
        'phone': '无',
        'food_type': '湖北菜',
        'description': '酱料浓郁，面条劲道，本地人喜爱的热干面馆',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '江岸区',
        'image_url': '/images/restaurants/restaurant_19.jpg' # 田师傅热干面
    },
    {
        'name': '毛肚火锅(街道口店)',
        'address': '武汉市洪山区街道口珞狮南路147号未来城购物中心5楼',
        'latitude': 30.5265,
        'longitude': 114.3518,
        'phone': '027-87668888',
        'food_type': '火锅',
        'description': '新鲜毛肚是特色，重庆风味麻辣火锅',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '洪山区',
        'image_url': '/images/restaurants/restaurant_20.jpg' # 毛肚火锅
    }
]

# 评价示例数据
def generate_sample_reviews(restaurant_ids):
    """根据餐厅ID生成评价数据"""
    reviews = []
    comments = [
        "味道很好，环境也不错。",
        "分量足，价格实惠。",
        "服务态度很好，下次会再来。",
        "味道一般，但环境不错。",
        "特色菜很推荐，其他一般。",
        "性价比高，值得推荐！",
        "地理位置很方便，交通便利。",
        "招牌菜很好吃，其他菜品一般。",
        "环境舒适，但价格偏高。",
        "服务有待提高，但食物不错。",
        "食材新鲜，烹饪技术一流。",
        "位置有点难找，但味道很赞。"
    ]
    user_names = [
        "武汉吃货",
        "美食探险家",
        "老饕",
        "吃吃喝喝",
        "麻辣爱好者",
        "甜点控",
        "川菜达人",
        "米其林评委",
        "武大学生",
        "游客"
    ]
    
    for restaurant_id in restaurant_ids:
        # 为每家餐厅生成3-7条评价
        num_reviews = random.randint(3, 7)
        for _ in range(num_reviews):
            review = {
                'restaurant_id': restaurant_id,
                'rating': random.randint(3, 5),  # 评分3-5星
                'comment': random.choice(comments),
                'user_name': random.choice(user_names)
            }
            reviews.append(review)
    
    return reviews

def seed_updated_data():
    """填充更新的测试数据"""
    app = create_app()
    with app.app_context():
        # !! 新增：先删除旧数据 (包括关联表) !!
        try:
            # 1. 先删除关联表中的数据
            # 使用 text() 构造原生SQL语句来删除关联表数据
            db.session.execute(text('DELETE FROM food_restaurant_association'))
            print("🧹 已删除 food_restaurant_association 表中的旧记录")

            # 2. 再删除路线停靠点数据 (新增)
            db.session.execute(text('DELETE FROM route_stop'))
            print("🧹 已删除 route_stop 表中的旧记录")

            # 3. 再删除评价数据
            num_deleted_reviews = db.session.query(Review).delete()
            print(f"🧹 已删除 {num_deleted_reviews} 条旧评价记录")

            # 4. 最后删除餐厅数据
            num_deleted_restaurants = db.session.query(Restaurant).delete()
            print(f"🧹 已删除 {num_deleted_restaurants} 条旧餐厅记录")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ 删除旧数据失败: {e}")
            return

        # 检查是否已有数据
        existing_restaurants = Restaurant.query.count()
        existing_reviews = Review.query.count()
        
        if existing_restaurants > 0:
            print(f"数据库中已有 {existing_restaurants} 条餐厅记录")
        else:
            # 添加示例餐厅数据
            added_restaurants = []
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
                added_restaurants.append(restaurant)
            
            db.session.commit()
            print(f"✅ 成功添加 {len(added_restaurants)} 条餐厅记录")
            
            # 获取所有餐厅ID
            restaurant_ids = [r.id for r in Restaurant.query.all()]
        
        if restaurant_ids:
            # 生成并添加评价数据
            review_data = generate_sample_reviews(restaurant_ids)
            for data in review_data:
                review = Review(
                    restaurant_id=data['restaurant_id'],
                    rating=data['rating'],
                    comment=data['comment'],
                    user_name=data['user_name']
                )
                db.session.add(review)
            
            db.session.commit()
            print(f"✅ 成功添加 {len(review_data)} 条评价记录")
        else:
            print("❌ 没有找到餐厅数据，无法添加评价")

if __name__ == '__main__':
    seed_updated_data() 