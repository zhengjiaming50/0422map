from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.food_culture import FoodCulture, FoodRoute, RouteStop
from app.models.restaurant import Restaurant

# 创建蓝图
food_culture_bp = Blueprint('food_culture', __name__, url_prefix='/api/food-culture')

# 获取所有美食文化信息
@food_culture_bp.route('/', methods=['GET'])
def get_food_cultures():
    try:
        food_type = request.args.get('food_type')
        district = request.args.get('district')
        
        query = FoodCulture.query
        
        if food_type:
            query = query.filter(FoodCulture.food_type == food_type)
        
        if district:
            query = query.filter(FoodCulture.origin_district == district)
            
        food_cultures = query.all()
        
        result = [{
            'id': fc.id,
            'name': fc.name,
            'description': fc.description,
            'history': fc.history,
            'making_method': fc.making_method,
            'image_url': fc.image_url,
            'food_type': fc.food_type,
            'origin_district': fc.origin_district,
            'restaurants': [{'id': r.id, 'name': r.name} for r in fc.restaurants]
        } for fc in food_cultures]
        
        return jsonify(result), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 获取指定ID的美食文化详情
@food_culture_bp.route('/<int:id>', methods=['GET'])
def get_food_culture(id):
    try:
        food_culture = FoodCulture.query.get(id)
        
        if not food_culture:
            return jsonify({'error': 'Food culture not found'}), 404
            
        result = {
            'id': food_culture.id,
            'name': food_culture.name,
            'description': food_culture.description,
            'history': food_culture.history,
            'making_method': food_culture.making_method,
            'image_url': food_culture.image_url,
            'food_type': food_culture.food_type,
            'origin_district': food_culture.origin_district,
            'restaurants': [{
                'id': r.id,
                'name': r.name,
                'address': r.address,
                'district': r.district,
                'image_url': r.image_url
            } for r in food_culture.restaurants]
        }
        
        return jsonify(result), 200
    
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# 获取美食类型列表
@food_culture_bp.route('/food-types', methods=['GET'])
def get_food_types():
    try:
        food_types = db.session.query(FoodCulture.food_type).distinct().all()
        return jsonify([ft[0] for ft in food_types if ft[0]]), 200
    
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# 获取发源地区列表
@food_culture_bp.route('/districts', methods=['GET'])
def get_origin_districts():
    try:
        districts = db.session.query(FoodCulture.origin_district).distinct().all()
        return jsonify([d[0] for d in districts if d[0]]), 200
    
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# 获取所有美食线路
@food_culture_bp.route('/routes', methods=['GET'])
def get_food_routes():
    try:
        district = request.args.get('district')
        
        query = FoodRoute.query
        
        if district:
            query = query.filter(FoodRoute.district == district)
            
        food_routes = query.all()
        
        result = [{
            'id': route.id,
            'name': route.name,
            'description': route.description,
            'image_url': route.image_url,
            'duration': route.duration,
            'district': route.district,
            'stops_count': len(route.stops)
        } for route in food_routes]
        
        return jsonify(result), 200
    
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# 获取指定ID的美食线路详情
@food_culture_bp.route('/routes/<int:id>', methods=['GET'])
def get_food_route(id):
    try:
        food_route = FoodRoute.query.get(id)
        
        if not food_route:
            return jsonify({'error': 'Food route not found'}), 404
            
        result = {
            'id': food_route.id,
            'name': food_route.name,
            'description': food_route.description,
            'image_url': food_route.image_url,
            'duration': food_route.duration,
            'district': food_route.district,
            'stops': [{
                'order': stop.stop_order,
                'visit_time': stop.visit_time,
                'recommendation': stop.recommendation,
                'restaurant': {
                    'id': stop.restaurant.id,
                    'name': stop.restaurant.name,
                    'address': stop.restaurant.address,
                    'latitude': stop.restaurant.latitude,
                    'longitude': stop.restaurant.longitude,
                    'food_type': stop.restaurant.food_type,
                    'image_url': stop.restaurant.image_url
                }
            } for stop in food_route.stops]
        }
        
        return jsonify(result), 200
    
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500 