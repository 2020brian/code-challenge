# app/app.py
from flask import Flask, render_template, jsonify, request
from app import app, db
from app.models import Hero, Powers, HeroPowers
from sqlalchemy.orm import joinedload

# Define your routes here

@app.route('/')
def index():
    heroes = Hero.query.all()
    return render_template('index.html', heroes=heroes)

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

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Powers.query.get(power_id)
    if power:
        try:
            data = request.get_json()
            power.description = data.get('description', power.description)
            db.session.commit()
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400
    else:
        return jsonify({"error": "Power not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)
