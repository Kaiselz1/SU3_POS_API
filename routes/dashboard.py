# from app import app

# @app.route('/')
from flask import Blueprint, render_template, current_app

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    return '<h1>dashboard</h1>'
