import os
from app import create_app, db
from app.models.restaurant import Restaurant

def check_image_files():
    # 创建Flask应用并设置上下文
    app = create_app()
    with app.app_context():
        # 查询所有餐厅记录
        restaurants = Restaurant.query.all()
        
        # 定义图片根目录
        image_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'wuhan-food-map', 'public')
        
        print(f"检查图片文件是否存在...")
        print(f"图片根目录: {image_root}")
        
        # 遍历所有餐厅记录并检查图片文件
        missing_images = []
        for restaurant in restaurants:
            if restaurant.image_url:
                # 移除URL开头的斜杠
                image_path = restaurant.image_url.lstrip('/')
                full_path = os.path.join(image_root, image_path)
                
                # 检查文件是否存在
                if not os.path.exists(full_path):
                    print(f"❌ 缺失: {restaurant.name} - {restaurant.image_url}")
                    missing_images.append((restaurant.id, restaurant.name, restaurant.image_url))
                    
                    # 尝试检查其他可能的扩展名
                    alternatives = [
                        full_path + '.png',
                        full_path.replace('.jpg', '.png'),
                        full_path.replace('.jpg', '.jpeg')
                    ]
                    
                    for alt_path in alternatives:
                        if os.path.exists(alt_path):
                            print(f"✅ 但找到替代文件: {os.path.basename(alt_path)}")
                            break
                else:
                    print(f"✅ 存在: {restaurant.name} - {restaurant.image_url}")
        
        # 打印结果摘要
        if missing_images:
            print(f"\n总共有 {len(missing_images)} 个餐厅图片缺失:")
            for id, name, url in missing_images:
                print(f"餐厅ID: {id} - {name} - {url}")
        else:
            print("\n所有餐厅图片文件都已存在!")

if __name__ == "__main__":
    check_image_files() 