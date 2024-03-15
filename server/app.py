# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id==id).first()

    if pet:
        body = pet.to_dict()
        status = 200
    else:
        status = 400
        body = {'message': f'Pet {id} not found.'}

    return make_response(body, status)

@app.route('/species/<string:species>')
def pest_by_species(species):
    pets = Pet.query.filter_by(species=species).all()
    pets_json = []
    for pet in pets:
        pets_json.append(pet.to_dict())
    
    body = {"pets": pets_json, 'count': len(pets)}

    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
