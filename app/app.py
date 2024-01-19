from flask import Flask, render_template, jsonify, request
from app import app, db
from app.models import Hero, Powers, HeroPowers
from sqlalchemy.orm import joinedload

# Define routes

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
    

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()

        required_fields = ['strength', 'power_id', 'hero_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"errors": [f"{field} is required"]}), 400

    
        allowed_strengths = ['Strong', 'Weak', 'Average']
        if data['strength'] not in allowed_strengths:
            return jsonify({"errors": [f"Invalid strength value. Allowed values are {', '.join(allowed_strengths)}"]}), 400

        
        power = Powers.query.get(data['power_id'])
        hero = Hero.query.get(data['hero_id'])
        if not power or not hero:
            return jsonify({"errors": ["Power or Hero not found"]}), 404

    
        hero_power = HeroPowers(
            strength=data['strength'],
            hero=hero,
            power=power
        )

        db.session.add(hero_power)
        db.session.commit()

        formatted_hero = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": p.id, "name": p.name, "description": p.description}
                for p in hero.hero_powers
            ]
        }

        return jsonify(formatted_hero), 201 
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400


if __name__ == '__main__':
    app.run(port=5555)
