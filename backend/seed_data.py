from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.review import Review
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
    print("餐厅评价数据添加完成。")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_data()
        seed_reviews()
        print("所有示例数据已添加完成。") 