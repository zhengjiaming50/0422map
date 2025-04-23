from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.review import Review
import random

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
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbjJS.jpg'
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
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbqEt.jpg'
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
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbXE8.jpg'
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
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbLdS.jpg'
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
        'image_url': 'https://z3.ax1x.com/2021/05/31/2Sb7rQ.jpg'
    },
    {
        'name': '武昌鱼馆',
        'address': '武汉市武昌区友谊大道128号',
        'latitude': 30.5326,
        'longitude': 114.3142,
        'phone': '027-88991234',
        'food_type': '湖北菜',
        'description': '正宗武昌鱼，百年老店',
        'business_hours': '周一至周日 10:00-21:30',
        'district': '武昌区',
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbHAg.jpg'
    },
    {
        'name': '江滩夜市烧烤',
        'address': '武汉市江岸区沿江大道与江边路交叉口',
        'latitude': 30.5862,
        'longitude': 114.3094,
        'phone': '027-88995678',
        'food_type': '烧烤',
        'description': '江边夜宵，啤酒烧烤',
        'business_hours': '周一至周日 18:00-03:00',
        'district': '江岸区',
        'image_url': 'https://z3.ax1x.com/2021/05/31/2SbOud.jpg'
    },
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
        
        if existing_reviews > 0:
            print(f"数据库中已有 {existing_reviews} 条评价记录")
        else:
            # 如果没有已存在的评价但有餐厅数据
            if 'restaurant_ids' not in locals():
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