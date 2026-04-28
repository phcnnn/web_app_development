from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 基本配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化擴充功能
    db.init_app(app)

    # 註冊 Blueprint
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app
