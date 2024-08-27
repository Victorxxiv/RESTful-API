from flask import Flask, request, jsonify, make_response, abort, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Resource(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"<Resource {self.name}>"

@app.route('/api/v1/resource', methods=['GET'])
def create_resource():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    # Process data
    return jsonify({'message': 'Resource created', 'data': data}), 201

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

@app.route('/api/v1/resource/<int:id', methods=['PUT'])
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


if __name__ == '__main__':
    app.run(debug=True)
