import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import app
from models import db, User, Transaction

# 模拟数据配置
CATEGORIES = {
    "支出": {
        "餐饮美食": [
            "美团外卖",
            "食堂午餐",
            "星巴克咖啡",
            "海底捞火锅",
            "瑞幸奶茶",
            "肯德基",
            "晚餐烧烤",
        ],
        "交通出行": ["滴滴打车", "地铁充值", "共享单车", "高铁票", "加油站", "泊车费"],
        "日常购物": [
            "淘宝下单",
            "超市买菜",
            "拼多多日用品",
            "名创优品",
            "优衣库衣服",
            "京东数码",
        ],
        "休闲娱乐": ["电影票", "Steam游戏", "B站大会员", "KTV聚会", "展览门票"],
        "生活服务": ["话费充值", "水费缴纳", "电费缴纳", "快递费"],
    },
    "收入": {
        "职业收入": ["实习工资", "项目奖金", "绩效奖金", "劳务报酬"],
        "理财": ["利息收入", "基金分红", "股票收益"],
        "人情往来": ["生日红包", "过年红包", "转账收回"],
    },
}


def seed_data():
    with app.app_context():
        # 安全检查：如果表不存在则创建，如果已存在则跳过（不会删除数据）
        db.create_all()

        # 检查 demo 用户是否已存在
        demo_user = User.query.filter_by(username="demo").first()

        if not demo_user:
            # 不存在则创建 demo 账号
            demo_user = User(username="demo", password=generate_password_hash("123321"))
            db.session.add(demo_user)
            db.session.commit()
            print(f"✅ 成功创建 demo 用户！密码：123321")
        else:
            print(f"ℹ️ 用户 {demo_user.username} 已存在，正在增量添加流水...")

        # 生成 50 条流水
        transactions = []
        now = datetime.now()

        for i in range(50):
            # 80% 几率生成支出，20% 生成收入
            t_type = random.choices(["支出", "收入"], weights=[0.8, 0.2])[0]

            if t_type == "支出":
                main_cat = random.choice(list(CATEGORIES["支出"].keys()))
                note = random.choice(CATEGORIES["支出"][main_cat])
                amount = round(random.uniform(5.0, 300.0), 2)
                # 模拟偶尔的大额消费
                if random.random() > 0.96:
                    amount = round(random.uniform(800, 2500), 2)
            else:
                main_cat = random.choice(list(CATEGORIES["收入"].keys()))
                note = random.choice(CATEGORIES["收入"][main_cat])
                amount = round(random.uniform(200.0, 6000.0), 2)

            # 生成过去 30 天内的随机时间点
            random_days = random.randint(0, 30)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            tx_time = now - timedelta(
                days=random_days, hours=random_hours, minutes=random_minutes
            )

            new_tx = Transaction(
                amount=amount,
                type=t_type,
                note=note,
                category_main=main_cat,
                category_sub="自动生成",  # 标记这是脚本生成的
                date=tx_time,
                user_id=demo_user.id,
            )
            transactions.append(new_tx)

        db.session.add_all(transactions)
        db.session.commit()
        print(
            f"🚀 成功为用户 '{demo_user.username}' 注入 {len(transactions)} 条示例流水！"
        )
        print(f"💡 现在你可以登录任意账号，它们的数据是完全隔离的。")


if __name__ == "__main__":
    seed_data()
