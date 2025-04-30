from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.review import Review
import random
from sqlalchemy import text, exc

sample_restaurants = [
    {
        'name': '宽窄巷子小吃店',
        'address': '成都市青羊区宽窄巷子1号',
        'latitude': 30.6717,
        'longitude': 104.0650,
        'phone': '028-88888888',
        'food_type': '川菜',
        'description': '以钵钵鸡、担担面等成都特色小吃为主',
        'business_hours': '周一至周日 9:00-22:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/bb1e003cfb3a2dcc.jpg' # 担担面
    },
    {
        'name': '春熙路步行街火锅',
        'address': '成都市锦江区春熙路步行街118号',
        'latitude': 30.6579,
        'longitude': 104.0809,
        'phone': '028-88889999',
        'food_type': '火锅',
        'description': '成都特色麻辣火锅，食材新鲜',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/62d33eec5be3ab00.jpg' # 麻辣火锅
    },
    {
        'name': '文殊院老龙抄手',
        'address': '成都市青羊区文殊院街66号',
        'latitude': 30.6755,
        'longitude': 104.0626,
        'phone': '028-88887777',
        'food_type': '小吃',
        'description': '百年老字号，专营成都著名抄手',
        'business_hours': '周一至周日 8:00-20:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/97ded6520cfcce71.jpg' # 抄手
    },
    {
        'name': '锦里烧烤',
        'address': '成都市武侯区锦里古街8号',
        'latitude': 30.6416,
        'longitude': 104.0474,
        'phone': '028-88886666',
        'food_type': '烧烤',
        'description': '特色烤鱼，秘制调料，外焦里嫩',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/b12701ac74927856.jpg' # 烤鱼
    },
    {
        'name': '天府广场西餐厅',
        'address': '成都市青羊区天府广场5号',
        'latitude': 30.6574,
        'longitude': 104.0653,
        'phone': '028-88885555',
        'food_type': '西餐',
        'description': '西式简餐，特色牛排和意面',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/43a568f975f96178.jpg' # 牛排
    },
    {
        'name': '老字号陈麻婆豆腐',
        'address': '成都市青羊区锦里中路88号',
        'latitude': 30.6494,
        'longitude': 104.0581,
        'phone': '028-88881111',
        'food_type': '川菜',
        'description': '正宗麻婆豆腐发源地，成都必吃',
        'business_hours': '周一至周日 6:00-21:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/0a3451e85cf5092d.jpg' # 麻婆豆腐
    },
    {
        'name': '四季美小笼包',
        'address': '成都市锦江区中山路668号',
        'latitude': 30.6598,
        'longitude': 104.0798,
        'phone': '028-88882222',
        'food_type': '小吃',
        'description': '皮薄馅足，汤汁鲜美的小笼包',
        'business_hours': '周一至周日 7:00-20:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/faafcd471bb22b65.jpg' # 小笼包
    },
    {
        'name': '蜀味馆总店',
        'address': '成都市锦江区大慈寺路232号',
        'latitude': 30.6507,
        'longitude': 104.0854,
        'phone': '028-88876543',
        'food_type': '川菜',
        'description': '正宗水煮鱼，麻辣鲜香',
        'business_hours': '周一至周日 10:00-21:30',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/2cd33f456fb5ebbe.jpg' # 水煮鱼
    },
    {
        'name': '成都冷吃兔',
        'address': '成都市锦江区春熙路1号',
        'latitude': 30.6577,
        'longitude': 104.0813,
        'phone': '028-88883333',
        'food_type': '小吃',
        'description': '麻辣鲜香的兔肉，成都特产',
        'business_hours': '周一至周日 10:00-23:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/17bee81dd2b0d9f0.jpg' # 冷吃兔
    },
    {
        'name': '玉林街夫妻肺片',
        'address': '成都市武侯区玉林北路文化路口',
        'latitude': 30.6305,
        'longitude': 104.0516,
        'phone': '无',
        'food_type': '小吃',
        'description': '鲜香麻辣的夫妻肺片，成都特色',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/94aa24a0976a2c79.jpg' # 夫妻肺片
    },
    {
        'name': '洞子口张老二凉粉',
        'address': '成都市武侯区科华北路洞子口',
        'latitude': 30.6312,
        'longitude': 104.0644,
        'phone': '无',
        'food_type': '小吃',
        'description': '地道成都凉粉，麻辣酸甜，清爽可口',
        'business_hours': '周一至周日 6:00-13:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/a1c13285b6ce86ee.jpg' # 凉粉
    },
    {
        'name': '杜甫草堂回锅肉',
        'address': '成都市青羊区杜甫草堂博物馆旁',
        'latitude': 30.6691,
        'longitude': 104.0343,
        'phone': '028-88884444',
        'food_type': '川菜',
        'description': '正宗川味回锅肉，肥而不腻',
        'business_hours': '周一至周日 10:30-21:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/8f43b94f1c879be5.jpg' # 回锅肉
    },
    {
        'name': '龙抄手总店',
        'address': '成都市锦江区人民东路18号',
        'latitude': 30.6624,
        'longitude': 104.0791,
        'phone': '028-82788888',
        'food_type': '川菜',
        'description': '成都老字号，抄手鲜嫩爽滑',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/e166efb6af9a00a8.jpg' # 龙抄手
    },
    {
        'name': '巴蜀大宅门(太古里店)',
        'address': '成都市锦江区太古里100号',
        'latitude': 30.6564,
        'longitude': 104.0823,
        'phone': '028-85777779',
        'food_type': '川菜',
        'description': '江湖菜是招牌，口味多样',
        'business_hours': '周一至周日 16:00-03:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/7127dc2f82c1eee5.jpg' # 江湖菜
    },
    {
        'name': '皇城老妈火锅(春熙路店)',
        'address': '成都市锦江区春熙路69号',
        'latitude': 30.6580,
        'longitude': 104.0805,
        'phone': '028-85757757',
        'food_type': '火锅',
        'description': '正宗川味火锅，红汤鲜香，油而不腻',
        'business_hours': '周一至周日 11:00-02:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/bfbfe8a969f888c3.jpg' # 红汤火锅
    },
    {
        'name': '串串香(九眼桥店)',
        'address': '成都市锦江区九眼桥附近',
        'latitude': 30.6489,
        'longitude': 104.0990,
        'phone': '028-87339999',
        'food_type': '串串香',
        'description': '种类丰富的串串香，麻辣爽口',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/45fa2b9cb507b7a7.jpg' # 串串香
    },
    {
        'name': '韦昌记锅盔(宽窄巷子店)',
        'address': '成都市青羊区宽窄巷子内',
        'latitude': 30.6717,
        'longitude': 104.0645,
        'phone': '无',
        'food_type': '小吃',
        'description': '正宗锅盔，外脆里软，口感丰富',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/66a63a18d7896617.jpg' # 锅盔
    },
    {
        'name': '赖汤圆(总府店)',
        'address': '成都市青羊区总府路33号',
        'latitude': 30.6656,
        'longitude': 104.0621,
        'phone': '028-82836840',
        'food_type': '小吃',
        'description': '汤圆皮薄馅足，甜咸均有',
        'business_hours': '周一至周日 7:00-20:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/df05772c766ee9ce.jpg' # 汤圆
    },
    {
        'name': '龙师傅担担面(双楠店)',
        'address': '成都市武侯区双楠路12号',
        'latitude': 30.6202,
        'longitude': 104.0274,
        'phone': '无',
        'food_type': '川菜',
        'description': '麻辣鲜香，面条劲道，本地人喜爱的担担面馆',
        'business_hours': '周一至周日 6:00-14:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/974d478f8867f264.jpg' # 担担面
    },
    {
        'name': '海底捞火锅(太古里店)',
        'address': '成都市锦江区太古里广场5楼',
        'latitude': 30.6563,
        'longitude': 104.0826,
        'phone': '028-87668888',
        'food_type': '火锅',
        'description': '服务一流的连锁火锅店，食材新鲜',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/75e80ee183170b5c.jpg' # 海底捞火锅
    },
    {
        'name': '青城山豆腐宴',
        'address': '成都市都江堰市青城山下街58号',
        'latitude': 30.9135,
        'longitude': 103.5668,
        'phone': '028-87111222',
        'food_type': '素食',
        'description': '道家风味素食，青城山特色豆腐菜系',
        'business_hours': '周一至周日 9:00-20:00',
        'district': '都江堰市',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/a8c45df9e17cc332.jpg' # 豆腐
    },
    {
        'name': '大熊猫茶餐厅',
        'address': '成都市成华区熊猫大道1375号',
        'latitude': 30.6776,
        'longitude': 104.1412,
        'phone': '028-83225566',
        'food_type': '茶点',
        'description': '融合川式茶文化的特色餐厅，提供精致茶点',
        'business_hours': '周一至周日 10:00-22:00',
        'district': '成华区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/c7a94fe21c88a943.jpg' # 茶点
    },
    {
        'name': '东郊记忆小酒馆',
        'address': '成都市成华区建设北路东二段4号',
        'latitude': 30.6698,
        'longitude': 104.1065,
        'phone': '028-84991234',
        'food_type': '酒吧',
        'description': '工业风格小酒馆，提供特色小吃和精酿啤酒',
        'business_hours': '周一至周日 16:00-02:00',
        'district': '成华区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/6b7df2a3c8e5f119.jpg' # 精酿啤酒
    },
    {
        'name': '双流黄龙溪古镇农家乐',
        'address': '成都市双流区黄龙溪古镇内',
        'latitude': 30.3105,
        'longitude': 103.9784,
        'phone': '028-85557777',
        'food_type': '农家菜',
        'description': '古镇特色农家菜，以本地食材为主打',
        'business_hours': '周一至周日 9:00-20:00',
        'district': '双流区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/1ad54e7fb21da865.jpg' # 农家菜
    },
    {
        'name': '金沙遗址博物馆咖啡厅',
        'address': '成都市青羊区金沙遗址路2号',
        'latitude': 30.6827,
        'longitude': 104.0134,
        'phone': '028-87303222',
        'food_type': '西式',
        'description': '博物馆内高雅咖啡厅，提供精致西式简餐',
        'business_hours': '周二至周日 9:00-17:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/98f5a31c7de22b87.jpg' # 咖啡厅
    },
    {
        'name': '天府新区创意餐厅',
        'address': '成都市天府新区天府大道1600号',
        'latitude': 30.5204,
        'longitude': 104.0665,
        'phone': '028-88998899',
        'food_type': '创意菜',
        'description': '融合川菜与西式烹饪理念的现代创意料理',
        'business_hours': '周一至周日 11:00-23:00',
        'district': '天府新区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/5e33f4d69a7b1c54.jpg' # 创意料理
    },
    {
        'name': '彭州丹景山农庄',
        'address': '成都市彭州市丹景山镇',
        'latitude': 31.0125,
        'longitude': 103.8965,
        'phone': '028-83778899',
        'food_type': '农家菜',
        'description': '山区特色农家菜，自产食材，原汁原味',
        'business_hours': '周一至周日 9:00-19:00',
        'district': '彭州市',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/3f44a25e8d7cc109.jpg' # 山区农家菜
    },
    {
        'name': '新都桂湖公园湖畔餐厅',
        'address': '成都市新都区新都街道桂湖路12号',
        'latitude': 30.8245,
        'longitude': 104.1586,
        'phone': '028-89894455',
        'food_type': '湖鲜',
        'description': '湖畔景观餐厅，以新鲜淡水鱼为特色',
        'business_hours': '周一至周日 10:30-21:30',
        'district': '新都区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/4a0b36fec98d7723.jpg' # 淡水鱼
    },
    {
        'name': '龙泉驿樱桃农场餐厅',
        'address': '成都市龙泉驿区洛带镇樱桃村',
        'latitude': 30.5612,
        'longitude': 104.2693,
        'phone': '028-84567788',
        'food_type': '农家菜',
        'description': '樱桃主题餐厅，提供当季水果和特色农家菜',
        'business_hours': '周一至周日 9:00-20:00',
        'district': '龙泉驿区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/7eaff4d69cb54322.jpg' # 樱桃主题
    },
    {
        'name': '大蓉和(紫荆店)',
        'address': '成都市武侯区紫荆南路52号',
        'latitude': 30.6288,
        'longitude': 104.0615,
        'phone': '028-85183355',
        'food_type': '川菜',
        'description': '知名川菜品牌，环境大气，适合宴请',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/11ab22cd33ef44gh.jpg' # 蓉和第一家
    },
    {
        'name': '自贡好吃客(科华店)',
        'address': '成都市武侯区科华北路60号',
        'latitude': 30.6375,
        'longitude': 104.0811,
        'phone': '028-85556999',
        'food_type': '自贡菜',
        'description': '以鲜锅兔、跳水蛙闻名的地道自贡盐帮菜',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/22bc33de44fg55hi.jpg' # 鲜锅兔
    },
    {
        'name': '饕林餐厅(IFS店)',
        'address': '成都市锦江区红星路三段1号IFS国际金融中心7楼',
        'latitude': 30.6572,
        'longitude': 104.0828,
        'phone': '028-86655888',
        'food_type': '创意川菜',
        'description': '环境优雅的创意川菜馆，菜品精致',
        'business_hours': '周一至周日 11:30-14:00, 17:30-21:30',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/33cd44ef55gh66ij.jpg' # 创意菜品
    },
    {
        'name': '银杏金阁(人民南路店)',
        'address': '成都市武侯区人民南路四段19号威斯顿联邦大厦',
        'latitude': 30.6410,
        'longitude': 104.0702,
        'phone': '028-85558888',
        'food_type': '粤菜/川菜',
        'description': '成都老牌高端餐饮，环境服务一流',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/44de55fg66hi77jk.jpg' # 高端宴请
    },
    {
        'name': '小谭豆花(西大街店)',
        'address': '成都市青羊区西大街86附13号',
        'latitude': 30.6741,
        'longitude': 104.0605,
        'phone': '028-86252753',
        'food_type': '小吃',
        'description': '成都著名豆花老字号，特色馓子豆花',
        'business_hours': '周一至周日 07:00-20:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/55ef66gh77ij88kl.jpg' # 馓子豆花
    },
    {
        'name': '三只耳冷锅鱼(倪家桥店)',
        'address': '成都市武侯区倪家桥路10号',
        'latitude': 30.6392,
        'longitude': 104.0723,
        'phone': '028-85575198',
        'food_type': '火锅',
        'description': '成都特色冷锅鱼，鱼肉鲜嫩，味道麻辣',
        'business_hours': '周一至周日 11:00-23:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/66fg77hi88jk99lm.jpg' # 冷锅鱼
    },
    {
        'name': '转转会(宽窄店)',
        'address': '成都市青羊区宽巷子10号',
        'latitude': 30.6715,
        'longitude': 104.0638,
        'phone': '028-86639933',
        'food_type': '新派川菜',
        'description': '位于宽窄巷子内，环境有特色，融合创新川菜',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/77gh88ij99kl00mn.jpg' # 院落餐厅
    },
    {
        'name': '马旺子川小馆(太古里店)',
        'address': '成都市锦江区东糠市街1号',
        'latitude': 30.6559,
        'longitude': 104.0835,
        'phone': '028-86661781',
        'food_type': '川菜',
        'description': '百年老字号川菜馆，招牌旺子血旺',
        'business_hours': '周一至周日 11:00-21:30',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/88hi99jk00lm11op.jpg' # 血旺
    },
    {
        'name': '柴门饭儿(高新店)',
        'address': '成都市高新区天府大道北段1700号环球中心E2',
        'latitude': 30.5678,
        'longitude': 104.0649,
        'phone': '028-87460666',
        'food_type': '川菜',
        'description': '时尚川菜馆，环境现代，适合年轻人聚餐',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '高新区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/99ij00kl11mn22pq.jpg' # 现代川菜
    },
    {
        'name': '红杏酒家(羊西店)',
        'address': '成都市金牛区羊西线蜀汉路426号',
        'latitude': 30.6855,
        'longitude': 104.0237,
        'phone': '028-87538888',
        'food_type': '川菜',
        'description': '老牌川菜馆，菜品稳定，分量足',
        'business_hours': '周一至周日 11:00-14:00, 17:00-21:00',
        'district': '金牛区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/00jk11lm22op33qr.jpg' # 红杏鸡
    },
    {
        'name': '锅锅香干锅(建设路店)',
        'address': '成都市成华区建设路54号附8号',
        'latitude': 30.6743,
        'longitude': 104.1059,
        'phone': '028-84311234',
        'food_type': '干锅',
        'description': '特色干锅，种类多样，味道浓郁',
        'business_hours': '周一至周日 11:00-23:00',
        'district': '成华区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/aabbccddeeff0011.jpg' # 干锅
    },
    {
        'name': '钟水饺(人民公园店)',
        'address': '成都市青羊区少城路12号人民公园内',
        'latitude': 30.6632,
        'longitude': 104.0585,
        'phone': '028-86133778',
        'food_type': '小吃',
        'description': '成都老字号小吃，红油水饺是特色',
        'business_hours': '周一至周日 08:00-19:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/bbccddeeffgg1122.jpg' # 钟水饺
    },
    {
        'name': '钢管厂五区小郡肝串串香(总店)',
        'address': '成都市金牛区抚琴街道办事处饮马河街48号附2号',
        'latitude': 30.6818,
        'longitude': 104.0497,
        'phone': '028-87789888',
        'food_type': '串串香',
        'description': '非常火爆的串串香店，小郡肝是必点',
        'business_hours': '周一至周日 17:00-03:00',
        'district': '金牛区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ccddeeffgghh2233.jpg' # 小郡肝串串
    },
    {
        'name': '何师烧烤(科华店)',
        'address': '成都市武侯区科华北路143号蓝色加勒比广场',
        'latitude': 30.6358,
        'longitude': 104.0809,
        'phone': '028-85551188',
        'food_type': '烧烤',
        'description': '环境时尚的烧烤店，烤五花肉很受欢迎',
        'business_hours': '周一至周日 17:00-02:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ddeeffgghhii3344.jpg' # 烤五花肉
    },
    {
        'name': '醉西昌(鸿云店)',
        'address': '成都市武侯区鸿云路11号附2号',
        'latitude': 30.6195,
        'longitude': 104.0642,
        'phone': '028-85008888',
        'food_type': '烧烤',
        'description': '西昌火盆烧烤，氛围很好，适合聚会',
        'business_hours': '周一至周日 17:00-01:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/eeffgghhiijj4455.jpg' # 火盆烧烤
    },
    {
        'name': '冒椒火辣(奎星楼店)',
        'address': '成都市青羊区奎星楼街33号',
        'latitude': 30.6725,
        'longitude': 104.0588,
        'phone': '028-86958785',
        'food_type': '串串香',
        'description': '网红串串店，冷锅串串和兔头是特色',
        'business_hours': '周一至周日 11:30-22:30',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ffgghhiijjkk5566.jpg' # 冷锅串串
    },
    {
        'name': '甘记肥肠粉(文殊院店)',
        'address': '成都市青羊区文殊院街18号',
        'latitude': 30.6761,
        'longitude': 104.0629,
        'phone': '无',
        'food_type': '小吃',
        'description': '地道成都肥肠粉，汤底浓郁，粉条爽滑',
        'business_hours': '周一至周日 07:00-18:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/gghhiijjkkll6677.jpg' # 肥肠粉
    },
    {
        'name': '甜水面(文殊院附近)',
        'address': '成都市青羊区酱园公所街58号',
        'latitude': 30.6759,
        'longitude': 104.0635,
        'phone': '无',
        'food_type': '小吃',
        'description': '面条粗壮有嚼劲，酱汁甜辣可口',
        'business_hours': '周一至周日 08:00-17:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/hhiijjkkllmm7788.jpg' # 甜水面
    },
    {
        'name': '贺记蛋烘糕(工人村店)',
        'address': '成都市金牛区内曹家巷工人村',
        'latitude': 30.6795,
        'longitude': 104.0682,
        'phone': '无',
        'food_type': '小吃',
        'description': '成都特色小吃蛋烘糕，口味选择多',
        'business_hours': '周一至周日 10:00-18:00 (不定时)',
        'district': '金牛区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/iijjkkllmmnn8899.jpg' # 蛋烘糕
    },
    {
        'name': '乐山跷脚牛肉(肖家河店)',
        'address': '成都市武侯区肖家河街43号附5号',
        'latitude': 30.6321,
        'longitude': 104.0495,
        'phone': '028-85177789',
        'food_type': '川菜',
        'description': '乐山特色美食，牛肉鲜嫩，汤底鲜美',
        'business_hours': '周一至周日 10:30-21:30',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/jjkkllmmnnoo9900.jpg' # 跷脚牛肉
    },
    {
        'name': '宽窄老茶馆',
        'address': '成都市青羊区窄巷子32号',
        'latitude': 30.6710,
        'longitude': 104.0630,
        'phone': '028-86661234',
        'food_type': '川菜',
        'description': '体验老成都慢生活，品盖碗茶，尝特色川菜',
        'business_hours': '周一至周日 10:00-22:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/kkllmmnnoopp0011.jpg' # 盖碗茶
    },
    {
        'name': '太古里精品火锅',
        'address': '成都市锦江区中纱帽街8号太古里F2',
        'latitude': 30.6568,
        'longitude': 104.0832,
        'phone': '028-87774321',
        'food_type': '火锅',
        'description': '环境优雅的精品火锅，食材考究，锅底地道',
        'business_hours': '周一至周日 11:00-00:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/llmmnnooppqq1122.jpg' # 精品火锅
    },
    {
        'name': '玉林路夜市小吃摊',
        'address': '成都市武侯区玉林西路与玉林南路交叉口',
        'latitude': 30.6300,
        'longitude': 104.0520,
        'phone': '无',
        'food_type': '小吃',
        'description': '集合多种成都地道小吃，夜宵好去处',
        'business_hours': '周一至周日 18:00-03:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/mmnnooppqqrr2233.jpg' # 夜市小吃
    },
    {
        'name': '建设路网红烧烤',
        'address': '成都市成华区建设巷1号附10号',
        'latitude': 30.6750,
        'longitude': 104.1055,
        'phone': '028-84339876',
        'food_type': '烧烤',
        'description': '电子科大附近网红烧烤店，种类丰富，味道巴适',
        'business_hours': '周一至周日 17:30-02:30',
        'district': '成华区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/nnooppqqrrss3344.jpg' # 网红烧烤
    },
    {
        'name': '环球中心云端餐厅',
        'address': '成都市高新区天府大道北段1700号环球中心W3栋顶层',
        'latitude': 30.5680,
        'longitude': 104.0655,
        'phone': '028-66885588',
        'food_type': '创意菜',
        'description': '俯瞰城南夜景，品味融合创意菜肴',
        'business_hours': '周一至周日 17:00-23:00',
        'district': '高新区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ooppqqrrsstt4455.jpg' # 云端餐厅
    },
    {
        'name': '抚琴小区地道串串',
        'address': '成都市金牛区抚琴西南街5号',
        'latitude': 30.6825,
        'longitude': 104.0480,
        'phone': '无',
        'food_type': '串串香',
        'description': '老小区里的地道串串香，味道正宗，价格亲民',
        'business_hours': '周一至周日 16:00-01:00',
        'district': '金牛区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ppqqrrssttuu5566.jpg' # 地道串串
    },
    {
        'name': '兴隆湖畔意式餐厅',
        'address': '成都市天府新区兴隆湖环湖路',
        'latitude': 30.4620,
        'longitude': 104.0680,
        'phone': '028-88112233',
        'food_type': '西餐',
        'description': '湖景优美的意式餐厅，提供正宗披萨和意面',
        'business_hours': '周一至周日 11:00-21:00',
        'district': '天府新区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/qqrrssttuuvv6677.jpg' # 意式餐厅
    },
    {
        'name': '机场路农家小院',
        'address': '成都市双流区机场路辅路旁',
        'latitude': 30.5700,
        'longitude': 103.9500,
        'phone': '028-85889900',
        'food_type': '农家菜',
        'description': '体验乡村风情，品尝新鲜地道的农家菜',
        'business_hours': '周一至周日 10:00-20:00',
        'district': '双流区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/rrssttuuvvww7788.jpg' # 农家小院
    },
    {
        'name': '人民公园钟水饺分店',
        'address': '成都市青羊区祠堂街9号',
        'latitude': 30.6625,
        'longitude': 104.0590,
        'phone': '028-86154577',
        'food_type': '小吃',
        'description': '紧邻人民公园，方便快捷品尝老字号钟水饺',
        'business_hours': '周一至周日 09:00-20:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ssttuuvvwwxx8899.jpg' # 钟水饺分店
    },
    {
        'name': '春熙路家常菜馆',
        'address': '成都市锦江区暑袜南街58号',
        'latitude': 30.6590,
        'longitude': 104.0800,
        'phone': '028-86751199',
        'food_type': '川菜',
        'description': '地处繁华春熙路，提供地道家常川菜，经济实惠',
        'business_hours': '周一至周日 10:30-21:30',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ttuuvvwwxxyy9900.jpg' # 家常菜馆
    },
    # 新增10家餐厅
    {
        'name': '大慈寺糖油果子',
        'address': '成都市青羊区大慈寺路23号',
        'latitude': 30.6745,
        'longitude': 104.0590,
        'phone': '028-83241567',
        'food_type': '小吃',
        'description': '传统成都早点，外酥里软，香甜可口',
        'business_hours': '周一至周日 6:00-12:00',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/aa12bb34cc56dd78.jpg' # 糖油果子
    },
    {
        'name': '太升南路老灶火锅',
        'address': '成都市青羊区太升南路125号',
        'latitude': 30.6680,
        'longitude': 104.0675,
        'phone': '028-86324590',
        'food_type': '火锅',
        'description': '传统老式火锅，铜锅煮制，香味浓郁',
        'business_hours': '周一至周日 11:00-22:30',
        'district': '青羊区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ee90ff12gg34hh56.jpg' # 老式火锅
    },
    {
        'name': '交子公园生态餐厅',
        'address': '成都市高新区天府大道北段666号',
        'latitude': 30.5859,
        'longitude': 104.0657,
        'phone': '028-85426789',
        'food_type': '创意菜',
        'description': '公园内高档餐厅，融合传统与现代的创意菜品',
        'business_hours': '周一至周日 11:00-22:00',
        'district': '高新区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ii78jj90kk12ll34.jpg' # 生态餐厅
    },
    {
        'name': '双桥子夜市烤串',
        'address': '成都市锦江区双桥子路夜市街',
        'latitude': 30.6670,
        'longitude': 104.0893,
        'phone': '无',
        'food_type': '烧烤',
        'description': '地道成都夜市烤串，种类丰富，价格亲民',
        'business_hours': '周一至周日 18:00-02:00',
        'district': '锦江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/mm56nn78oo90pp12.jpg' # 夜市烤串
    },
    {
        'name': '浣花溪公园茶楼',
        'address': '成都市武侯区浣花溪公园内',
        'latitude': 30.6330,
        'longitude': 104.0210,
        'phone': '028-87654321',
        'food_type': '茶点',
        'description': '古典园林式茶楼，提供精致茶点和四川特色小吃',
        'business_hours': '周一至周日 8:30-18:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/qq34rr56ss78tt90.jpg' # 园林茶楼
    },
    {
        'name': '科华北路豆花面馆',
        'address': '成都市武侯区科华北路89号',
        'latitude': 30.6320,
        'longitude': 104.0820,
        'phone': '028-85551234',
        'food_type': '面食',
        'description': '特色豆花面和酸辣粉，口味独特，深受当地人喜爱',
        'business_hours': '周一至周日 7:00-20:00',
        'district': '武侯区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/uu12vv34ww56xx78.jpg' # 豆花面
    },
    {
        'name': '成华区蛋烘糕',
        'address': '成都市成华区建设北路二段15号',
        'latitude': 30.6784,
        'longitude': 104.1075,
        'phone': '无',
        'food_type': '小吃',
        'description': '传统成都蛋烘糕，松软可口，现烤现卖',
        'business_hours': '周一至周日 7:30-19:30',
        'district': '成华区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/yy90zz12ab34cd56.jpg' # 蛋烘糕
    },
    {
        'name': '温江钵钵鸡',
        'address': '成都市温江区柳城大道99号',
        'latitude': 30.6821,
        'longitude': 103.8466,
        'phone': '028-82345678',
        'food_type': '川菜',
        'description': '正宗温江钵钵鸡，麻辣鲜香，鸡肉嫩滑',
        'business_hours': '周一至周日 10:00-21:00',
        'district': '温江区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/ef78gh90ij12kl34.jpg' # 钵钵鸡
    },
    {
        'name': '五块石粉蒸肉',
        'address': '成都市金牛区五块石路45号',
        'latitude': 30.6925,
        'longitude': 104.0620,
        'phone': '028-83456789',
        'food_type': '川菜',
        'description': '传统川菜粉蒸肉，香糯入味，搭配米饭绝佳',
        'business_hours': '周一至周日 11:00-21:00',
        'district': '金牛区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/mn56op78qr90st12.jpg' # 粉蒸肉
    },
    {
        'name': '双流区国际风味餐厅',
        'address': '成都市双流区东升街道学府路34号',
        'latitude': 30.5788,
        'longitude': 104.0120,
        'phone': '028-88991234',
        'food_type': '国际料理',
        'description': '机场附近国际风味餐厅，提供多国特色美食',
        'business_hours': '周一至周日 10:00-22:00',
        'district': '双流区',
        'image_url': 'https://cdn-fusion.imgcdn.store/i/2025/uv34wx56yz78ab90.jpg' # 国际料理
    }
]

# 评价示例数据
def generate_sample_reviews(restaurant_ids):
    """根据餐厅ID生成评价数据"""
    reviews = []
    comments = [
        "味道很好，环境也不错。",
        "分量足，价格实惠。",
        "服务态度很好，下次会再来。",
        "味道一般，但环境不错。",
        "特色菜很推荐，其他一般。",
        "性价比高，值得推荐！",
        "地理位置很方便，交通便利。",
        "招牌菜很好吃，其他菜品一般。",
        "环境舒适，但价格偏高。",
        "服务有待提高，但食物不错。",
        "食材新鲜，烹饪技术一流。",
        "位置有点难找，但味道很赞。"
    ]
    user_names = [
        "成都吃货",
        "美食探险家",
        "老饕",
        "吃吃喝喝",
        "麻辣爱好者",
        "甜点控",
        "川菜达人",
        "米其林评委",
        "川大学生",
        "游客"
    ]
    
    for restaurant_id in restaurant_ids:
        # 为每家餐厅生成3-7条评价
        num_reviews = random.randint(3, 7)
        for _ in range(num_reviews):
            review = {
                'restaurant_id': restaurant_id,
                'rating': random.randint(3, 5),  # 评分3-5星
                'comment': random.choice(comments),
                'user_name': random.choice(user_names)
            }
            reviews.append(review)
    
    return reviews

def seed_updated_data():
    """填充更新的测试数据"""
    app = create_app()
    with app.app_context():
        # !! 新增：先删除旧数据 (包括关联表) !!
        try:
            # 1. 尝试删除关联表中的数据，如果表不存在则忽略错误
            try:
                db.session.execute(text('DELETE FROM food_restaurant_association'))
                print("🧹 已删除 food_restaurant_association 表中的旧记录")
            except exc.ProgrammingError as e:
                db.session.rollback()
                print("ℹ️ food_restaurant_association 表不存在，跳过")

            # 2. 尝试删除路线停靠点数据
            try:
                db.session.execute(text('DELETE FROM route_stop'))
                print("🧹 已删除 route_stop 表中的旧记录")
            except exc.ProgrammingError as e:
                db.session.rollback()
                print("ℹ️ route_stop 表不存在，跳过")

            # 3. 再删除评价数据
            num_deleted_reviews = db.session.query(Review).delete()
            print(f"🧹 已删除 {num_deleted_reviews} 条旧评价记录")

            # 4. 最后删除餐厅数据
            num_deleted_restaurants = db.session.query(Restaurant).delete()
            print(f"🧹 已删除 {num_deleted_restaurants} 条旧餐厅记录")

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"❌ 删除旧数据失败: {e}")
            return

        # 检查是否已有数据
        existing_restaurants = Restaurant.query.count()
        existing_reviews = Review.query.count()
        
        if existing_restaurants > 0:
            print(f"数据库中已有 {existing_restaurants} 条餐厅记录")
        else:
            # 添加示例餐厅数据
            added_restaurants = []
            for data in sample_restaurants:
                restaurant = Restaurant(
                    name=data['name'],
                    address=data['address'],
                    latitude=data['latitude'],
                    longitude=data['longitude'],
                    phone=data['phone'],
                    food_type=data['food_type'],
                    description=data['description'],
                    business_hours=data['business_hours'],
                    district=data['district'],
                    image_url=data['image_url']
                )
                db.session.add(restaurant)
                added_restaurants.append(restaurant)
            
            db.session.commit()
            print(f"✅ 成功添加 {len(added_restaurants)} 条餐厅记录")
            
        # 获取所有餐厅ID
        restaurant_ids = [r.id for r in Restaurant.query.all()]
        
        if restaurant_ids:
            # 生成并添加评价数据
            review_data = generate_sample_reviews(restaurant_ids)
            for data in review_data:
                review = Review(
                    restaurant_id=data['restaurant_id'],
                    rating=data['rating'],
                    comment=data['comment'],
                    user_name=data['user_name']
                )
                db.session.add(review)
            
            db.session.commit()
            print(f"✅ 成功添加 {len(review_data)} 条评价记录")
        else:
            print("❌ 没有找到餐厅数据，无法添加评价")

if __name__ == '__main__':
    seed_updated_data() 