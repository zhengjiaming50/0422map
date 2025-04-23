import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    """应用配置类"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_wuhan_food_map')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/wuhan_food_map'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 其他配置
    ROWS_PER_PAGE = 20
    
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/wuhan_food_map_test'
    )
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
# 根据环境变量选择配置
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# 默认使用开发环境配置
Config = config_by_name[os.environ.get('FLASK_ENV', 'development')] 