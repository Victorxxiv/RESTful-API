from flask import Flask, request, jsonify, make_response, abort, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

@app.route('/api/v1/resource', methods=['GET'])
def create_resource():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    # Process data
    return jsonify({'messafe': 'Resource created', 'data': data}), 201


if __name__ == '__main__':
    app.run(debug=True)
