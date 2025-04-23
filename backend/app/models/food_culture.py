from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# 美食和餐厅的多对多关联表
food_restaurant_association = db.Table(
    'food_restaurant_association',
    db.Column('food_id', db.Integer, db.ForeignKey('food_culture.id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'), primary_key=True)
)

class FoodCulture(db.Model):
    """武汉特色美食文化模型"""
    __tablename__ = 'food_culture'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment="美食名称")
    description = db.Column(db.Text, nullable=False, comment="美食介绍")
    history = db.Column(db.Text, nullable=True, comment="历史背景")
    making_method = db.Column(db.Text, nullable=True, comment="制作方法")
    image_url = db.Column(db.String(255), nullable=True, comment="美食图片")
    food_type = db.Column(db.String(50), nullable=True, comment="美食类型")
    origin_district = db.Column(db.String(50), nullable=True, comment="发源地区")
    
    # 关联到餐厅，可选
    restaurants = db.relationship("Restaurant", secondary=food_restaurant_association)

    def __repr__(self):
        return f"<FoodCulture {self.name}>"


class FoodRoute(db.Model):
    """一日美食线路推荐模型"""
    __tablename__ = 'food_route'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment="线路名称")
    description = db.Column(db.Text, nullable=False, comment="线路介绍")
    image_url = db.Column(db.String(255), nullable=True, comment="线路图片")
    duration = db.Column(db.String(50), nullable=True, comment="推荐游览时间")
    district = db.Column(db.String(50), nullable=True, comment="所在区域")
    
    # 线路包含的餐厅列表，按顺序排列
    stops = db.relationship("RouteStop", back_populates="route", order_by="RouteStop.stop_order")

    def __repr__(self):
        return f"<FoodRoute {self.name}>"


class RouteStop(db.Model):
    """线路站点模型，记录线路中的餐厅顺序"""
    __tablename__ = 'route_stop'

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('food_route.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False, comment="站点顺序")
    visit_time = db.Column(db.String(50), nullable=True, comment="推荐游览时间")
    recommendation = db.Column(db.Text, nullable=True, comment="推荐菜品或建议")
    
    # 关系
    route = db.relationship("FoodRoute", back_populates="stops")
    restaurant = db.relationship("Restaurant")

    def __repr__(self):
        return f"<RouteStop {self.route_id}-{self.restaurant_id}>" 