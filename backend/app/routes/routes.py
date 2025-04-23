from flask import Blueprint, request, jsonify
import requests
import os
import polyline
import json
from datetime import datetime

# 创建蓝图
routes_bp = Blueprint('routes', __name__)

# 使用Mapbox Directions API作为路线规划服务
# 实际开发中应从环境变量获取API密钥
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhlbmdqaWFtaW5nIiwiYSI6ImNtOXM1ZTViaTA0dTIyanI1OHVjMDZrOW8ifQ.awqJ-KNyvXXq4drMK7HqWw'
MAPBOX_DIRECTIONS_API = 'https://api.mapbox.com/directions/v5/mapbox'

@routes_bp.route('/', methods=['GET'])
def get_route():
    """获取两点之间的路线规划"""
    try:
        # 获取请求参数
        start_lng = request.args.get('start_lng')
        start_lat = request.args.get('start_lat')
        end_lng = request.args.get('end_lng')
        end_lat = request.args.get('end_lat')
        mode = request.args.get('mode', 'walking')  # 默认步行
        
        # 验证必要参数
        if not all([start_lng, start_lat, end_lng, end_lat]):
            return jsonify({
                "error": "缺少必要参数",
                "required": ["start_lng", "start_lat", "end_lng", "end_lat"]
            }), 400
        
        # 验证参数格式
        try:
            start_lng = float(start_lng)
            start_lat = float(start_lat)
            end_lng = float(end_lng)
            end_lat = float(end_lat)
        except ValueError:
            return jsonify({"error": "坐标参数必须为数值类型"}), 400
        
        # 地图模式映射
        mode_mapping = {
            'walking': 'walking',   # 步行
            'driving': 'driving',   # 驾车
            'transit': 'driving'    # 公交（简化为驾车，实际应使用公交API）
        }
        
        mapbox_mode = mode_mapping.get(mode, 'walking')
        
        # 构建API请求
        coordinates = f"{start_lng},{start_lat};{end_lng},{end_lat}"
        url = f"{MAPBOX_DIRECTIONS_API}/{mapbox_mode}/{coordinates}"
        
        params = {
            'access_token': MAPBOX_ACCESS_TOKEN,
            'geometries': 'geojson',
            'steps': 'true',
            'language': 'zh',
            'overview': 'full'
        }
        
        # 发送请求到Mapbox API
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return jsonify({
                "error": "路线规划服务错误",
                "details": response.text
            }), 500
        
        # 解析响应数据
        route_data = response.json()
        
        # 检查是否有路线结果
        if not route_data.get('routes') or len(route_data['routes']) == 0:
            return jsonify({"error": "无法找到路线"}), 404
        
        # 获取第一条路线
        route = route_data['routes'][0]
        
        # 提取路线信息
        legs = route.get('legs', [])
        
        # 格式化导航步骤
        steps = []
        for leg in legs:
            for step in leg.get('steps', []):
                steps.append({
                    'instruction': step.get('maneuver', {}).get('instruction', ''),
                    'distance': step.get('distance', 0),
                    'duration': step.get('duration', 0),
                    'maneuver': step.get('maneuver', {}).get('type', 'unknown')
                })
        
        # 构建响应数据
        result = {
            'geometry': route.get('geometry', {}),
            'distance': route.get('distance', 0),  # 米
            'duration': route.get('duration', 0),  # 秒
            'steps': steps
        }
        
        return jsonify(result)
        
    except Exception as e:
        # 记录错误
        print(f"路线规划错误: {str(e)}")
        return jsonify({"error": f"路线规划过程中发生错误: {str(e)}"}), 500

# 模拟路线规划
def get_mock_route(start_coords, end_coords, mode):
    """生成模拟路线数据（用于测试或API不可用时）"""
    # 构建模拟几何数据
    mock_geometry = {
        "type": "LineString",
        "coordinates": [
            [start_coords[0], start_coords[1]],
            # 中间添加几个模拟的路径点
            [start_coords[0] + (end_coords[0] - start_coords[0]) * 0.25, 
             start_coords[1] + (end_coords[1] - start_coords[1]) * 0.25],
            [start_coords[0] + (end_coords[0] - start_coords[0]) * 0.5, 
             start_coords[1] + (end_coords[1] - start_coords[1]) * 0.5],
            [start_coords[0] + (end_coords[0] - start_coords[0]) * 0.75, 
             start_coords[1] + (end_coords[1] - start_coords[1]) * 0.75],
            [end_coords[0], end_coords[1]]
        ]
    }
    
    # 计算模拟距离（米）和时间（秒）
    # 实际项目中应使用更准确的距离计算公式
    import math
    
    def haversine(lon1, lat1, lon2, lat2):
        """
        计算两点间的距离（公里）
        """
        # 将经纬度转换为弧度
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        
        # haversine公式
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371  # 地球半径（公里）
        return c * r
    
    # 计算直线距离（公里）
    distance_km = haversine(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
    distance_m = distance_km * 1000  # 转换为米
    
    # 模拟不同模式的速度和路线长度系数
    mode_factors = {
        'walking': {'speed': 1.2, 'path_factor': 1.2},  # 步行 4.3 km/h, 路线系数1.2
        'driving': {'speed': 8.3, 'path_factor': 1.3},  # 驾车 30 km/h, 路线系数1.3
        'transit': {'speed': 4.2, 'path_factor': 1.5}   # 公交 15 km/h, 路线系数1.5
    }
    
    factor = mode_factors.get(mode, mode_factors['walking'])
    
    # 调整后的距离和时间
    adjusted_distance = distance_m * factor['path_factor']
    duration_seconds = (adjusted_distance / 1000) / factor['speed'] * 3600
    
    # 生成模拟导航步骤
    steps = [
        {
            'instruction': '出发，沿道路向前走',
            'distance': adjusted_distance * 0.3,
            'duration': duration_seconds * 0.3,
            'maneuver': 'depart'
        },
        {
            'instruction': '继续直行',
            'distance': adjusted_distance * 0.4,
            'duration': duration_seconds * 0.4,
            'maneuver': 'straight'
        },
        {
            'instruction': '到达目的地',
            'distance': adjusted_distance * 0.3,
            'duration': duration_seconds * 0.3,
            'maneuver': 'arrive'
        }
    ]
    
    return {
        'geometry': mock_geometry,
        'distance': adjusted_distance,
        'duration': duration_seconds,
        'steps': steps
    } 