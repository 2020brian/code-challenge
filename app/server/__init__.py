
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    db.init_app(app)

    # Import and register blueprints/routes here
    from backend.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app

app = create_app()
