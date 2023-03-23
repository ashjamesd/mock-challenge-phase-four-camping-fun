from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)


@app.route('/')
def index():
    response = make_response(
        {
            "message": "Hello Campers!"
        },
        200
    )
    return response



@app.route('/campers', methods = ['GET'])
def campers():
    campers = Camper.query.all()
    campers_dict = [camper.to_dict(rules = ('-signups',)) for camper in campers]

    response = make_response(
        jsonify(campers_dict)
        200
    )
    return response 

@app.route('/campers/<int:id>', methods = ['GET'])
def camper_by_id(id):
    camper=Camper.query.filter_by(id=id).first()

    if camper:

        camper_dict = camper.to_dict()

        response = make_response(
            jsonify(camper_dict),
            200
        )
    
    else:

        response = make_response({
            "error": "Camper not found"},
            404
        )
    return response

@app.route('/campers', methods = ['POST'])
def campers():
    try:
        new_camper = Camper(
            name = request.get_json()['name'],
            age = request.get_json()['age']
        )

        db.session.add(new_camper)
        db.session.commit()

        camper = Camper.query.filter(Camper.id == new_camper.camper_id).first()
        camper_dict = camper.to_dict()

        reponse = make_response(
            jsonify(camper_dict),
            201
        )

    except ValueError:

        response = make_response(
            {"errors": ["validation errors"]},
            400
        )

    return response



@app.route('/signups', methods = ['POST'])
def signups():
    try:
        new_signup = Signup(
            time = request.get_json()['time'],
            camper_id = request.get_json()['camper_id']
            activity_id = request.get_json()['activity_id']
        )

        db.session.add(new_signup)
        db.session.commit()

        camper = Camper.query.filter(Camper.id == new_signup.camper_id).first()
        camper_dict = camper.to_dict()

        reponse = make_response(
            jsonify(camper_dict),
            201
        )

    except ValueError:

        response = make_response(
            {"errors": ["validation errors"]},
            400
        )

    return response


@app.route('/activities', methods = ['GET'])
def activities():
    activities = Activity.query.all()
    activities_dict = [activity.to_dict(rules = ('-signups',)) for activity in activities]

    response = make_response(
        jsonify(activities_dict)
        200
    )
    return response

@app.route('/activities/<int:id>', methods = ['DELETE'])
def activities_by_id_delete(id):
    activity = Activity.query.get(id)
    db.session.delete(activity)
    db.session.commit



if __name__ == '__main__':
    app.run(port=5555, debug=True)


