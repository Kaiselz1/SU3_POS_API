import os
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# config the location the db will be create
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

app = Flask(__name__, instance_path=INSTANCE_DIR, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models  # Ensure models are imported for migration
import routes  # Ensure routes are imported

if __name__ == '__main__':
    app.run()