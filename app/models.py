from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the association table for the many-to-many relationship
hero_powers_association = db.Table(
    'hero_powers_association',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id')),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'))
)

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # One-to-Many relationship with HeroPowers
    hero_powers = db.relationship('HeroPowers', back_populates='hero')

class Powers(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Many-to-Many relationship with HeroPowers
    hero_powers = db.relationship('HeroPowers', back_populates='power')

class HeroPowers(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Define relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Powers', back_populates='hero_powers')
