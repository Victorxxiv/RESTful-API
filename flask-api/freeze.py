from flask_frozen import Freezer
from app import app  # Import the app from your Flask app file

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()