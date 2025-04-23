from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config.settings import Config

# 初始化SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=Config):
    # 创建Flask应用
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    
    # 配置CORS
    CORS(app)
    
    # 注册蓝图
    from app.routes.restaurants import restaurant_bp
    from app.routes.routes import routes_bp
    from app.routes.food_culture import food_culture_bp
    
    app.register_blueprint(restaurant_bp, url_prefix='/api')
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(food_culture_bp)
    
    @app.route('/api/health')
    def health_check():
        return {"status": "success", "message": "API服务正常运行"}
    
    return app 