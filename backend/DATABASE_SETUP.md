# 武汉美食地图数据库设置指南

本文档提供设置PostgreSQL数据库和PostGIS扩展的详细步骤，用于武汉美食地图系统。

## 1. 安装PostgreSQL

### Windows系统

1. 下载安装包：访问 [PostgreSQL官方下载页面](https://www.postgresql.org/download/windows/)
2. 运行安装程序，按照向导安装PostgreSQL
3. 安装时请记住设置的管理员密码
4. 完成安装后，Stack Builder会启动，勾选PostGIS空间扩展并安装

### MacOS系统

使用Homebrew:
```bash
brew install postgresql
brew services start postgresql
```

### Linux系统(Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

## 2. 安装PostGIS扩展

### Windows系统

如果在PostgreSQL安装时使用Stack Builder安装了PostGIS，则无需额外步骤。

### MacOS系统

```bash
brew install postgis
```

### Linux系统(Ubuntu/Debian)

```bash
sudo apt install postgis postgresql-13-postgis-3
```

## 3. 创建数据库

使用PostgreSQL命令行工具创建数据库:

```bash
# 连接到PostgreSQL
psql -U postgres

# 在PostgreSQL命令行中创建数据库
CREATE DATABASE wuhan_food_map;

# 连接到新创建的数据库
\c wuhan_food_map

# 为数据库启用PostGIS扩展
CREATE EXTENSION postgis;

# 验证PostGIS安装
SELECT PostGIS_version();
```

## 4. 配置后端连接

编辑项目根目录下的`.env`文件(如不存在则创建):

```
# 数据库连接
DATABASE_URL=postgresql://postgres:你的密码@localhost:5432/wuhan_food_map
```

## 5. 初始化数据库表

运行项目提供的数据库初始化脚本:

```bash
# 在后端项目根目录下执行
python init_db.py
```

## 6. 填充测试数据

运行项目提供的测试数据填充脚本:

```bash
# 在后端项目根目录下执行
python seed_data.py
```

## 7. 数据库备份与恢复

### 备份数据库

```bash
pg_dump -U postgres -d wuhan_food_map > wuhan_food_map_backup.sql
```

### 恢复数据库

```bash
psql -U postgres -d wuhan_food_map < wuhan_food_map_backup.sql
```

## 8. 常见问题解决

1. **无法连接到数据库**
   - 检查PostgreSQL服务是否运行
   - 验证用户名和密码是否正确
   - 确认主机和端口是否正确

2. **PostGIS函数不可用**
   - 确认已成功创建PostGIS扩展
   - 尝试重新创建扩展: `CREATE EXTENSION postgis;`

3. **权限问题**
   - 确保数据库用户有足够权限
   - 可能需要执行: `GRANT ALL PRIVILEGES ON DATABASE wuhan_food_map TO postgres;` 