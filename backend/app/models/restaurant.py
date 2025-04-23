from datetime import datetime
from geoalchemy2 import Geometry
from app import db

class Restaurant(db.Model):
    """餐厅数据模型"""
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # 使用PostGIS的Point类型存储地理位置
    location = db.Column(Geometry(geometry_type='POINT', srid=4326))
    phone = db.Column(db.String(20))
    food_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    business_hours = db.Column(db.String(200))
    district = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, address, latitude, longitude, food_type=None, 
                 district=None, phone=None, description=None, image_url=None, 
                 business_hours=None):
        self.name = name
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        # 创建PostGIS Point: 'POINT(longitude latitude)'
        self.location = f'POINT({longitude} {latitude})'
        self.phone = phone
        self.food_type = food_type
        self.description = description
        self.image_url = image_url
        self.business_hours = business_hours
        self.district = district
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'food_type': self.food_type,
            'description': self.description,
            'image_url': self.image_url,
            'business_hours': self.business_hours,
            'district': self.district
        } 