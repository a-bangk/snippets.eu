from flask import Blueprint

write_bp = Blueprint('write_bp', __name__)

from app.write import write


