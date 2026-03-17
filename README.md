# 💰 SLL记账 (SLL Finance)

**SLL记账** 是一款专为追求极致视觉体验的用户打造的轻量级个人财务管理系统。该项目作为“五年一贯制专转本”毕业设计开发，核心理念是将 **Apple 风格的极简主义（Minimalism）** 与 **液态玻璃（Glassmorphism）设计** 相结合，通过流畅的动效提供直观的收支分析。

---

## 🌟 项目亮点

* **极致视觉动效**：采用 `Stagger Load`（交错加载）动画，每一笔账单都以平滑的物理曲线划入视野。
* **AI 智能分类**：内置规则引擎，输入“吃火锅”自动识别为“餐饮美食”，无需手动选择。
* **多用户逻辑隔离**：支持多账号注册登录，采用数据库外键技术确保各用户数据物理共存、逻辑绝对隔离。
* **响应式数据看板**：集成 Chart.js，支持饼图（分布分析）与折线图（趋势分析）的无缝丝滑切换。

---

## 🏗️ 系统架构

本项目采用经典的前后端分离思想（在 Flask 框架下整合）：

* **后端 (Backend)**: Python 3.x + Flask 框架。
* **数据库 (Database)**: SQLite 3（文件型数据库，无需配置复杂环境）。
* **前端 (Frontend)**: Tailwind CSS (CSS 框架) + Chart.js (可视化引擎) + Web Animations API (动效)。
* **认证 (Auth)**: Flask-Login + Werkzeug (密码 Hash 加密)。

---

## 🚀 快速开始

### 1. 环境准备

确保你的电脑已安装 Python 3.8 或更高版本。

### 2. 创建并激活虚拟环境 (Venv)

在项目根目录下运行以下命令，这能保证项目依赖不污染你的系统环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

```

### 3. 安装依赖项

```bash
pip install flask flask_sqlalchemy flask_login flask_wtf wtforms

```

### 4. 注入示例数据 (可选)

如果你想立即看到精美的图表效果，可以运行种子数据脚本：

```bash
python init_demo.py

```

* **演示账号**：`demo`
* **演示密码**：`123321`

### 5. 运行项目

```bash
python app.py

```

访问浏览器：`http://127.0.0.1:5000`

---

## 📅 功能演示说明

### 🔐 用户认证系统

* 支持新用户注册，密码通过 `pbkdf2:sha256` 算法加密存储，保障信息安全。

### 📊 智能仪表盘

* **个性化问候**：主页根据登录账号动态展示“你好，Sun Lilong”。
* **动态结余**：自动计算当前账号的总收入、总支出及净结余。

### 📝 沉浸式记账

* 点击“快速记账”唤起半透明玻璃感遮罩层。
* 支持金额自动校验及备注关键词智能分类。

### 📈 数据可视化

* **分类分析**：直观展示餐饮、交通、购物等各项占比。
* **趋势追踪**：自动生成最近 30 天的财务波动曲线。

---

## 📁 项目目录结构

```text
SLL_Finance/
├── app.py              # 程序主入口，包含路由逻辑
├── models.py           # 数据库模型定义 (User, Transaction)
├── forms.py            # 表单验证逻辑
├── init_demo.py        # 演示数据注入脚本
├── static/             # 静态资源 (CSS, JS, Images)
├── templates/          # HTML 模板文件夹
│   ├── base.html       # 基础布局
│   ├── index.html      # 主看板页面
│   ├── login.html      # 登录页面
│   └── register.html   # 注册页面
├── sll_finance.db      # SQLite 数据库文件 (运行后生成)
└── README.md           # 项目说明文档

```

---

## 👨‍💻 开发信息

**开发者**：Lilong.sn