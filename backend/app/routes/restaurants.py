from flask import Blueprint, request, jsonify
from sqlalchemy import func
from geoalchemy2 import Geometry
from app import db
from app.models.restaurant import Restaurant
from app.models.review import Review

# 创建蓝图
restaurant_bp = Blueprint('restaurants', __name__)

@restaurant_bp.route('/restaurants/', methods=['GET'])
def get_restaurants():
    """获取餐厅列表，支持筛选"""
    # 获取查询参数
    district = request.args.get('district', '')
    food_type = request.args.get('food_type', '')
    query = request.args.get('query', '')
    
    # 创建查询
    restaurants_query = Restaurant.query
    
    # 应用筛选条件
    if district:
        restaurants_query = restaurants_query.filter(Restaurant.district == district)
    if food_type:
        restaurants_query = restaurants_query.filter(Restaurant.food_type == food_type)
    if query:
        search = f"%{query}%"
        restaurants_query = restaurants_query.filter(
            (Restaurant.name.ilike(search)) | (Restaurant.description.ilike(search))
        )
    
    # 执行查询
    restaurants = restaurants_query.all()
    
    # 转换为JSON格式
    result = [restaurant.to_dict() for restaurant in restaurants]
    
    return jsonify(result)

@restaurant_bp.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    """获取指定ID的餐厅详情"""
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify(restaurant.to_dict())

@restaurant_bp.route('/restaurants/districts', methods=['GET'])
def get_districts():
    """获取所有区域列表"""
    districts = db.session.query(Restaurant.district).distinct().filter(Restaurant.district != None).all()
    return jsonify([district[0] for district in districts])

@restaurant_bp.route('/restaurants/food-types', methods=['GET'])
def get_food_types():
    """获取所有美食类型列表"""
    food_types = db.session.query(Restaurant.food_type).distinct().filter(Restaurant.food_type != None).all()
    return jsonify([food_type[0] for food_type in food_types])

@restaurant_bp.route('/restaurants/density', methods=['GET'])
def get_restaurants_density():
    """获取餐厅密度数据，用于热力图显示"""
    try:
        # 获取筛选参数
        district = request.args.get('district', '')
        food_type = request.args.get('food_type', '')

        # 创建基础查询
        restaurants_query = Restaurant.query
        
        # 应用筛选条件
        if district:
            restaurants_query = restaurants_query.filter(Restaurant.district == district)
        if food_type:
            restaurants_query = restaurants_query.filter(Restaurant.food_type == food_type)
        
        restaurants = restaurants_query.all()
        
        # 计算餐厅密度
        # 这里我们使用一个简单的算法：统计每个餐厅附近其他餐厅的数量，作为其权重
        density_data = []
        
        for restaurant in restaurants:
            # 创建点几何体
            point = func.ST_SetSRID(func.ST_MakePoint(restaurant.longitude, restaurant.latitude), 4326)
            
            # 计算1公里内餐厅数量
            nearby_count = db.session.query(func.count(Restaurant.id)).filter(
                Restaurant.id != restaurant.id,
                func.ST_DWithin(Restaurant.location, point, 0.01)  # 约1公里
            ).scalar()
            
            # 设置权重上限为10（可根据实际数据调整）
            weight = min(nearby_count + 1, 10)
            
            density_data.append({
                'id': restaurant.id, 
                'latitude': restaurant.latitude,
                'longitude': restaurant.longitude,
                'weight': weight
            })
            
        return jsonify(density_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@restaurant_bp.route('/restaurants/nearby', methods=['GET'])
def get_nearby_restaurants():
    """获取指定坐标附近的餐厅"""
    try:
        # 获取参数
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        distance = float(request.args.get('distance', 2))  # 默认2公里
        
        # 创建点几何体
        point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
        
        # 查询距离在指定范围内的餐厅
        restaurants_query = Restaurant.query.filter(
            func.ST_DWithin(
                Restaurant.location,
                point,
                distance / 111.0  # 粗略转换为度
            )
        )
        
        # 添加距离信息
        restaurants_with_distance = []
        for restaurant in restaurants_query.all():
            restaurant_dict = restaurant.to_dict()
            # 计算距离（公里）
            distance_query = db.session.query(
                func.ST_Distance(
                    Restaurant.location,
                    point
                ) * 111.0  # 粗略转换为公里
            ).filter(Restaurant.id == restaurant.id).scalar()
            
            restaurant_dict['distance_km'] = round(distance_query, 2)
            restaurants_with_distance.append(restaurant_dict)
        
        # 按距离排序
        restaurants_with_distance.sort(key=lambda x: x['distance_km'])
        
        return jsonify(restaurants_with_distance)
    
    except (ValueError, TypeError) as e:
        return jsonify({"error": "无效的参数格式"}), 400

@restaurant_bp.route('/restaurants/bbox', methods=['GET'])
def get_restaurants_in_bbox():
    """获取指定边界框内的餐厅"""
    try:
        # 获取边界框参数
        min_lat = float(request.args.get('min_lat'))
        min_lng = float(request.args.get('min_lng'))
        max_lat = float(request.args.get('max_lat'))
        max_lng = float(request.args.get('max_lng'))
        
        # 创建边界框几何体
        bbox = func.ST_MakeEnvelope(min_lng, min_lat, max_lng, max_lat, 4326)
        
        # 查询边界框内的餐厅
        restaurants = Restaurant.query.filter(
            func.ST_Within(Restaurant.location, bbox)
        ).all()
        
        return jsonify([restaurant.to_dict() for restaurant in restaurants])
    
    except (ValueError, TypeError) as e:
        return jsonify({"error": "无效的参数格式"}), 400

@restaurant_bp.route('/restaurants/stats/by-district', methods=['GET'])
def get_stats_by_district():
    """获取按区域统计的餐厅数量"""
    stats = db.session.query(
        Restaurant.district,
        func.count(Restaurant.id).label('count')
    ).filter(Restaurant.district != None).group_by(Restaurant.district).all()
    
    return jsonify([{"district": stat[0], "count": stat[1]} for stat in stats])

@restaurant_bp.route('/restaurants/stats/by-food-type', methods=['GET'])
def get_stats_by_food_type():
    """获取按美食类型统计的餐厅数量"""
    stats = db.session.query(
        Restaurant.food_type,
        func.count(Restaurant.id).label('count')
    ).filter(Restaurant.food_type != None).group_by(Restaurant.food_type).all()
    
    return jsonify([{"food_type": stat[0], "count": stat[1]} for stat in stats])

@restaurant_bp.route('/restaurants/<int:restaurant_id>/reviews', methods=['GET'])
def get_restaurant_reviews(restaurant_id):
    """获取指定餐厅的评价列表"""
    # 确认餐厅存在
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # 获取评价列表
    reviews = Review.query.filter_by(restaurant_id=restaurant_id).order_by(Review.created_at.desc()).all()
    
    # 转换为JSON格式
    result = [review.to_dict() for review in reviews]
    
    # 计算平均评分
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    return jsonify({
        "restaurant_id": restaurant_id,
        "reviews": result,
        "avg_rating": round(avg_rating, 1),
        "total_reviews": len(reviews)
    })

@restaurant_bp.route('/restaurants/<int:restaurant_id>/reviews', methods=['POST'])
def add_restaurant_review(restaurant_id):
    """添加餐厅评价"""
    # 确认餐厅存在
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    try:
        # 获取请求数据
        data = request.json
        
        # 验证必要字段
        if not data or 'rating' not in data:
            return jsonify({"error": "评分为必填字段"}), 400
        
        # 验证评分范围
        rating = int(data['rating'])
        if rating < 1 or rating > 5:
            return jsonify({"error": "评分必须在1到5之间"}), 400
        
        # 创建评价记录
        review = Review(
            restaurant_id=restaurant_id,
            rating=rating,
            comment=data.get('comment'),
            user_name=data.get('user_name')
        )
        
        # 保存到数据库
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            "message": "评价添加成功",
            "review": review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400 