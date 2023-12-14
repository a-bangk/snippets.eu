from flask import Blueprint

filter_bp = Blueprint('filter_bp', __name__)

from app.filter import filter


