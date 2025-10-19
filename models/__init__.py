from flask_sqlalchemy import SQLAlchemy

# Central db object
db = SQLAlchemy()

from models.category import *
from models.customer import *
from models.product import *
from models.sale_item import *
from models.sale import *
from models.user import *
