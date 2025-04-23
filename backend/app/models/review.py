from datetime import datetime
from app import db

class Review(db.Model):
    """用户评价数据模型"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5星评分
    comment = db.Column(db.Text)
    user_name = db.Column(db.String(50))  # 可选用户名
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 与餐厅的关系
    restaurant = db.relationship('Restaurant')
    
    def __init__(self, restaurant_id, rating, comment=None, user_name=None):
        self.restaurant_id = restaurant_id
        self.rating = min(max(rating, 1), 5)  # 确保评分在1-5之间
        self.comment = comment
        self.user_name = user_name
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'rating': self.rating,
            'comment': self.comment,
            'user_name': self.user_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 