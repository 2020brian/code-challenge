from flask import Flask
from flask_migrate import Migrate

from models import db, Hero, Powers, HeroPowers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

if __name__ == '__main__':
    app.run(port=5555)
