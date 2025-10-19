import os
from flask import Flask
from flask_migrate import Migrate
from models import db  # central db
from models import *
from routes.user import user_bp
from routes import *

# config the location the db will be create
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

app = Flask(__name__, instance_path=INSTANCE_DIR, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)

if __name__ == '__main__':
    # app.run()
    with app.app_context():
        db.create_all()  # optional
    app.run(debug=True)