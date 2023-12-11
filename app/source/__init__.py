from flask import Blueprint


source_bp = Blueprint('source_bp', __name__)

from app.source import source
from app.source import management as sm


