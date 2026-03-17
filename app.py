from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Transaction
from forms import LoginForm, RegisterForm
import csv, io, json
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "sll-secret-key-2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sll_finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_ai_category(note):
    rules = {
        "餐饮美食": {
            "三餐": ["饭", "早", "中", "晚", "吃", "食堂"],
            "零食饮料": ["奶茶", "咖啡", "零食", "水果", "甜品"],
            "外卖": ["美团", "饿了么", "麦当劳", "肯德基"],
        },
        "交通出行": {
            "打车": ["滴滴", "出租", "T3", "高德"],
            "公共交通": ["地铁", "公交", "共享单车"],
            "长途": ["高铁", "飞机", "油", "泊车"],
        },
        "日常购物": {
            "超市": ["超市", "便利店", "7-11", "全家"],
            "网购": ["淘宝", "京东", "拼多多", "闲鱼"],
            "服饰": ["衣服", "鞋", "包"],
        },
        "休闲娱乐": {
            "游戏": ["充值", "网易", "腾讯", "Steam", "Switch"],
            "影视": ["电影", "视频", "会员", "B站"],
            "聚会": ["KTV", "剧本杀", "密室"],
        },
        "生活服务": {
            "缴费": ["水费", "电费", "话费", "网费"],
            "医疗": ["药", "挂号", "医院", "诊所"],
            "房租": ["租房", "房贷", "中介"],
        },
        "个人提升": {
            "教育": ["书", "课程", "考试", "报名"],
            "运动": ["健身", "球", "运动鞋"],
        },
        "人情往来": {"红包": ["转账", "红包", "份子钱"], "礼物": ["送礼", "鲜花"]},
        "职业收入": {
            "工资": ["月薪", "发工资", "绩效"],
            "兼职": ["外快", "劳务", "佣金"],
            "理财": ["利息", "红利", "投资"],
        },
    }
    for main, subs in rules.items():
        for sub, keywords in subs.items():
            if any(k in note for k in keywords):
                return main, sub
    return "随机支出", "其他"


@app.route("/")
@login_required
def index():
    txs = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.date.asc())
        .all()
    )
    exp_data, inc_data, trend_data = {}, {}, {}
    for t in txs:
        date_str = t.date.strftime("%m-%d")
        if date_str not in trend_data:
            trend_data[date_str] = {"exp": 0, "inc": 0}
        if t.type == "支出":
            exp_data[t.category_main] = exp_data.get(t.category_main, 0) + t.amount
            trend_data[date_str]["exp"] += t.amount
        else:
            inc_data[t.category_main] = inc_data.get(t.category_main, 0) + t.amount
            trend_data[date_str]["inc"] += t.amount
    return render_template(
        "index.html",
        txs=txs[::-1],
        exp_total=round(sum(exp_data.values()), 2),
        inc_total=round(sum(inc_data.values()), 2),
        exp_json=json.dumps(exp_data),
        inc_json=json.dumps(inc_data),
        trend_json=json.dumps(trend_data),
    )


@app.route("/add", methods=["POST"])
@login_required
def add():
    amount = float(request.form.get("amount", 0))
    note = request.form.get("note", "")
    t_type = request.form.get("type", "支出")
    if amount > 0:
        main_cat, sub_cat = get_ai_category(note)
        new_t = Transaction(
            amount=amount,
            type=t_type,
            note=note,
            category_main=main_cat,
            category_sub=sub_cat,
            user_id=current_user.id,
        )
        db.session.add(new_t)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    t = Transaction.query.get_or_404(id)
    if t.user_id == current_user.id:
        db.session.delete(t)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
