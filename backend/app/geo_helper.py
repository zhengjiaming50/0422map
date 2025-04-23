from sqlalchemy import func
from geoalchemy2 import Geometry

class GeoHelper:
    """地理空间查询辅助类"""
    
    @staticmethod
    def point_from_coords(lng, lat, srid=4326):
        """从经纬度创建点几何体"""
        return func.ST_SetSRID(func.ST_MakePoint(lng, lat), srid)
    
    @staticmethod
    def calculate_distance(point1, point2):
        """计算两点之间的距离（公里）"""
        # 使用PostGIS的ST_Distance_Sphere函数计算球面距离（米）
        # 然后除以1000转换为公里
        return func.ST_Distance_Sphere(point1, point2) / 1000
    
    @staticmethod
    def create_bbox(min_lng, min_lat, max_lng, max_lat, srid=4326):
        """创建边界框几何体"""
        return func.ST_MakeEnvelope(min_lng, min_lat, max_lng, max_lat, srid)
    
    @staticmethod
    def within_distance(point1, point2, distance_km):
        """检查两点之间的距离是否在指定公里数内"""
        # 将公里转换为米
        distance_m = distance_km * 1000
        return func.ST_DWithin(point1, point2, distance_m, False) 