#!/usr/bin/env python
import os
import sys
import subprocess
import platform
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库配置
db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:1@localhost:5432/wuhan_food_map')
test_db_url = os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:1@localhost:5432/wuhan_food_map_test')

# 解析数据库URL
def parse_db_url(url):
    # 解析格式：postgresql://username:password@host:port/dbname
    parts = url.replace('postgresql://', '').split('@')
    credentials = parts[0].split(':')
    host_db = parts[1].split('/')
    host_port = host_db[0].split(':')
    
    return {
        'username': credentials[0],
        'password': credentials[1],
        'host': host_port[0],
        'port': host_port[1] if len(host_port) > 1 else '5432',
        'dbname': host_db[1]
    }

def create_database(db_info):
    """创建PostgreSQL数据库并启用PostGIS扩展"""
    # 构建psql命令的环境变量
    env = os.environ.copy()
    env['PGPASSWORD'] = db_info['password']
    
    # 先检查数据库是否存在 (使用更可靠的方法)
    try:
        # 尝试连接到数据库，如果连接成功，则数据库存在
        connect_cmd = [
            'psql',
            '-U', db_info['username'],
            '-h', db_info['host'],
            '-p', db_info['port'],
            '-d', db_info['dbname'],
            '-c', "SELECT 1;"
        ]
        
        result = subprocess.run(connect_cmd, capture_output=True, text=True, env=env)
        
        # 如果能连接成功，返回码应该是0
        if result.returncode == 0:
            print(f"数据库 '{db_info['dbname']}' 已存在")
            
            # 检查PostGIS扩展是否已启用
            check_postgis_cmd = [
                'psql',
                '-U', db_info['username'],
                '-h', db_info['host'],
                '-p', db_info['port'],
                '-d', db_info['dbname'],
                '-c', "SELECT extname FROM pg_extension WHERE extname = 'postgis';"
            ]
            
            postgis_result = subprocess.run(check_postgis_cmd, capture_output=True, text=True, env=env)
            
            if "postgis" in postgis_result.stdout:
                print(f"PostGIS扩展已在数据库 '{db_info['dbname']}' 中启用")
            else:
                # 启用PostGIS扩展
                enable_postgis_cmd = [
                    'psql',
                    '-U', db_info['username'],
                    '-h', db_info['host'],
                    '-p', db_info['port'],
                    '-d', db_info['dbname'],
                    '-c', "CREATE EXTENSION IF NOT EXISTS postgis;"
                ]
                subprocess.run(enable_postgis_cmd, check=True, env=env)
                print(f"✅ PostGIS扩展在数据库 '{db_info['dbname']}' 中启用成功")
                
            return True
    except Exception:
        # 如果连接失败，数据库可能不存在，继续创建
        pass
    
    # 创建数据库
    try:
        create_cmd = [
            'psql',
            '-U', db_info['username'],
            '-h', db_info['host'],
            '-p', db_info['port'],
            '-c', f"CREATE DATABASE {db_info['dbname']};"
        ]
        subprocess.run(create_cmd, check=True, env=env)
        print(f"✅ 数据库 '{db_info['dbname']}' 创建成功")
        
        # 启用PostGIS扩展
        enable_postgis_cmd = [
            'psql',
            '-U', db_info['username'],
            '-h', db_info['host'],
            '-p', db_info['port'],
            '-d', db_info['dbname'],
            '-c', "CREATE EXTENSION IF NOT EXISTS postgis;"
        ]
        subprocess.run(enable_postgis_cmd, check=True, env=env)
        print(f"✅ PostGIS扩展在数据库 '{db_info['dbname']}' 中启用成功")
    
    except subprocess.CalledProcessError as e:
        if "already exists" in str(e):
            print(f"数据库 '{db_info['dbname']}' 已存在，跳过创建步骤")
            return True
        else:
            print(f"❌ 数据库操作失败: {e}")
            return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False
    
    return True

def check_postgresql_installation():
    """检查PostgreSQL是否已安装"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 检测到PostgreSQL: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL未安装或未添加到PATH中")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL未安装或未添加到PATH中")
        return False

def setup_databases():
    """设置开发和测试数据库"""
    # 检查PostgreSQL安装
    if not check_postgresql_installation():
        print_installation_guide()
        return
    
    # 创建主数据库
    main_db_info = parse_db_url(db_url)
    if create_database(main_db_info):
        print(f"✅ 主数据库 '{main_db_info['dbname']}' 设置完成")
    
    # 创建测试数据库
    test_db_info = parse_db_url(test_db_url)
    if create_database(test_db_info):
        print(f"✅ 测试数据库 '{test_db_info['dbname']}' 设置完成")

def print_installation_guide():
    """打印PostgreSQL和PostGIS安装指南"""
    os_name = platform.system()
    
    print("\n===== PostgreSQL & PostGIS 安装指南 =====")
    
    if os_name == 'Windows':
        print("""
Windows安装步骤:
1. 下载并安装PostgreSQL: https://www.postgresql.org/download/windows/
   - 安装过程中选择PostGIS扩展
   - 记住设置的管理员密码
2. 确保将PostgreSQL的bin目录添加到PATH环境变量
3. 重新启动命令行，然后再次运行此脚本
        """)
    elif os_name == 'Darwin':  # macOS
        print("""
macOS安装步骤:
1. 使用Homebrew安装:
   $ brew install postgresql postgis
2. 启动PostgreSQL服务:
   $ brew services start postgresql
3. 重新启动终端，然后再次运行此脚本
        """)
    else:  # Linux
        print("""
Linux (Ubuntu/Debian)安装步骤:
1. 安装PostgreSQL和PostGIS:
   $ sudo apt update
   $ sudo apt install postgresql postgresql-contrib postgis
2. 启动PostgreSQL服务:
   $ sudo systemctl start postgresql
   $ sudo systemctl enable postgresql
3. 重新启动终端，然后再次运行此脚本
        """)

if __name__ == '__main__':
    setup_databases()