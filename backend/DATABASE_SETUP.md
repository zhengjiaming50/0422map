# 武汉美食地图数据库设置指南

本文档提供武汉美食地图系统所需的PostgreSQL和PostGIS数据库设置指南。

## 系统要求

- PostgreSQL 12+
- PostGIS 3.0+
- Python 3.8+

## 安装PostgreSQL和PostGIS（stack）

### Windows

1. 下载并安装PostgreSQL：
   - 访问[PostgreSQL官方下载页面](https://www.postgresql.org/download/windows/)
   - 下载适合您系统的安装包
   - 运行安装程序
   - 安装过程中选择PostGIS扩展
   - 记住设置的管理员密码
   - 确保将PostgreSQL的bin目录添加到PATH环境变量

2. 验证安装：
   - 打开命令提示符或PowerShell
   - 运行 `psql --version` 确认PostgreSQL已安装
   - 运行 `psql -U postgres -c "SELECT PostGIS_version();"` 确认PostGIS已安装

### macOS

1. 使用Homebrew安装：
   ```bash
   brew install postgresql postgis
   ```

2. 启动PostgreSQL服务：
   ```bash
   brew services start postgresql
   ```

### Linux (Ubuntu/Debian)

1. 安装PostgreSQL和PostGIS：
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib postgis
   ```

2. 启动PostgreSQL服务：
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

## 数据库设置

在安装完PostgreSQL和PostGIS后，需要创建应用所需的数据库。您可以选择以下方法之一：

### 方法1：使用自动化脚本(推荐)

1. 克隆项目后，进入项目根目录

2. 确保已安装所需的Python包：
   ```bash
   pip install -r backend/requirements.txt
   ```

3. 运行数据库设置脚本：
   ```bash
   cd backend
   python setup_database.py
   ```
   
   此脚本将自动：
   - 检查PostgreSQL是否已安装
   - 创建开发和测试数据库
   - 在这些数据库中启用PostGIS扩展

### 方法2：手动设置

如果您希望手动设置数据库，请按照以下步骤操作：

1. 登录PostgreSQL：
   ```bash
   psql -U postgres
   ```

2. 创建数据库：
   ```sql
   CREATE DATABASE wuhan_food_map;
   CREATE DATABASE wuhan_food_map_test;
   ```

3. 为每个数据库启用PostGIS扩展：
   ```sql
   \c wuhan_food_map
   CREATE EXTENSION postgis;
   
   \c wuhan_food_map_test
   CREATE EXTENSION postgis;
   ```

## 初始化数据库表

1. 创建应用所需的表：
   ```bash
   cd backend
   python init_db.py
   ```

2. 添加测试数据：
   ```bash
   python update_seed_data.py
   ```

## 常见问题解决

### 无法连接到数据库

- 确认PostgreSQL服务正在运行
- 验证用户名和密码是否正确
- 检查.env文件中的数据库连接字符串

### 无法创建PostGIS扩展

- 确认已正确安装PostGIS
- 在Windows上，检查是否在PostgreSQL安装过程中选择了PostGIS扩展
- 在Linux上，尝试重新安装PostGIS：`sudo apt install postgis postgresql-<版本>-postgis-<版本>`

### 找不到psql命令

- 确保PostgreSQL的bin目录已添加到系统PATH环境变量中
- Windows: 添加 `C:\Program Files\PostgreSQL\<版本>\bin` 到PATH
- 重启终端或命令提示符

## 数据库模型

### Restaurant (餐厅)
- `id`: 主键
- `name`: 餐厅名称
- `address`: 地址
- `latitude`: 纬度
- `longitude`: 经度
- `location`: 地理位置点 (PostGIS格式)
- `phone`: 联系电话
- `food_type`: 美食类型
- `description`: 描述
- `image_url`: 图片链接
- `business_hours`: 营业时间
- `district`: 所在区域
- `created_at`: 创建时间
- `updated_at`: 更新时间

### Review (评价)
- `id`: 主键
- `restaurant_id`: 餐厅ID (外键)
- `rating`: 评分 (1-5星)
- `comment`: 评论内容
- `user_name`: 用户名
- `created_at`: 创建时间 