from flask import Blueprint

login_bp = Blueprint('login_bp', __name__)

from app.authentication import authentication


