import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)

# database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URI']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

# access all models
from models import *

# access all routes
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
