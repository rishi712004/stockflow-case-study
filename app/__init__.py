from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.product_routes import product_bp
    from app.routes.alert_routes import alert_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(alert_bp)

    return app