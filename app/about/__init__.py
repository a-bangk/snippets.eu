from flask import Blueprint

about_bp = Blueprint('about_bp', __name__)

from app.about import about


