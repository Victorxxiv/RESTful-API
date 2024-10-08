from functools import wraps
from flask import Flask, request, jsonify, make_response, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import stripe
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

stripe.api_key = "your_secret_key"

def require_auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != "expected_token":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrap

class Resource(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"<Resource {self.name}>"

class ResourrceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

class Resource:
    def __init__(self, name, description):
        self.id = None
        self.name = name
        self.description = description

# Serialize example
@app.route('/serialize', methods=['POST'])
def serialize():
    resource = Resource(name="Example", description="Example description")
    serialized_data = resource_schema.dump(resource)
    return jsonify(serialized_data)

# Validation example
@app.route('/validate', methods=['POST'])
def validate_data():
    input_data = request.get_json()
    errors = resource_schema.validate(input_data)
    if errors:
        return jsonify(errors), 400
    return jsonify({"message": "Data is valid!"})

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity={"username": "Victor"})
    return jsonify(access_token=access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(logged_in_as= "Victor")

@app.route('/api/v1/resource', methods=['POST'])
def create_resource():
    data = request.get_json()
    new_resource = Resource(name=data['name'], description=data['description', ''])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({'message': 'Resource created'}), 201

@app.route('/api/v1/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    resources_list = [{"id": r.id, "name": r.name, "description": r.description} for r in resources]
    return jsonify(resources_list), 200

@app.route('/api/v1/resource/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get(id)
    if resource:
        data = request.get_json()
        resource.name = data['name']
        resource.description = data.get('description', resource.description)
        db.session.commit()
        return jsonify({'message': 'Resource updated'}), 200
    return jsonify({'message': 'Resource not found'}), 404

@app.route('/api/v1/resource/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get(id)
    if resource:
        db.session.delete(resource)
        db.session.commit()
        return jsonify({'message': 'Resource deleted'}), 200
    return jsonify({'message': 'Resource not found'}), 404

@app.route('/api/v1/protected_resource', methods=['GET'])
@require_auth
def protected_resource():
    return jsonify({"message": "This is a protected resource"})

# Stripe API for payment processing
@app.route('/api/v1/charge', methods=['POST'])
def create_charge():
    data = request.get_json()
    charge = stripe.Charge.create(
        amount=data['amount'],
        currency='usd',
        source=data['token'],
        description='Charge for service'
    )
    return jsonify(charge), 201

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="An internal error occurred"), 500


if __name__ == '__main__':
    app.run(debug=True)
