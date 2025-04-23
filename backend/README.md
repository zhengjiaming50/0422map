# 武汉美食地图后端

这是武汉美食地图项目的后端部分，基于Flask框架开发，使用PostgreSQL/PostGIS提供地理空间数据支持。

## 功能特性

- RESTful API设计
- 基于PostgreSQL的地理空间查询
- 餐厅数据管理
- 空间分析与统计

## 快速开始

### 环境要求

- Python 3.8+
- PostgreSQL 13+
- PostGIS 3.0+

### 安装步骤

1. 克隆仓库
```bash
git clone <仓库地址>
cd wuhan-food-map/backend
```

2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 设置数据库
参考 `DATABASE_SETUP.md` 文件完成PostgreSQL和PostGIS的安装配置

5. 初始化数据库
```bash
python init_db.py
```

6. 添加测试数据
```bash
python seed_data.py
```

7. 启动服务器
```bash
python run.py
```

现在，API服务运行在 http://localhost:5000/

## API接口

- `GET /api/health` - 健康检查
- `GET /api/restaurants/` - 获取餐厅列表，支持筛选
- `GET /api/restaurants/<id>` - 获取餐厅详情
- `GET /api/restaurants/districts` - 获取区域列表
- `GET /api/restaurants/food-types` - 获取美食类型列表
- `GET /api/restaurants/nearby` - 获取附近餐厅
- `GET /api/restaurants/bbox` - 获取边界框内的餐厅
- `GET /api/restaurants/stats/by-district` - 按区域统计餐厅
- `GET /api/restaurants/stats/by-food-type` - 按美食类型统计餐厅

更多详细API文档，请参考项目根目录下的`接口文档.md`。

## 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── models/             # 数据模型
│   ├── routes/             # API路由
│   ├── schemas/            # 数据验证模式
│   └── geo_helper.py       # 地理空间查询辅助模块
├── config/                 # 配置目录
├── tests/                  # 测试目录
├── run.py                  # 应用入口
├── init_db.py              # 数据库初始化脚本
├── seed_data.py            # 测试数据脚本
└── DATABASE_SETUP.md       # 数据库设置文档
``` 