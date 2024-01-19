from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Powers, HeroPowers
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Define your routes here

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    formatted_heroes = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes
    ]
    return jsonify(formatted_heroes)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        formatted_hero = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": power.id, "name": power.name, "description": power.description}
                for power in hero.hero_powers
            ]
        }
        return jsonify(formatted_hero)
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Powers.query.all()
    formatted_powers = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(formatted_powers)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power_by_id(power_id):
    power = Powers.query.get(power_id)
    if power:
        formatted_power = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(formatted_power)
    else:
        return jsonify({"error": "Power not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)
