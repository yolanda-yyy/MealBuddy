from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# PostgreSQL 连接配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:116096@localhost/meetbuddy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 显式导出给外部模块使用
__all__ = ['db', 'app']
