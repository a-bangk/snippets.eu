from flask import Blueprint


source_bp = Blueprint('source_bp', __name__)

# Can i just delete these two lines?
# no, this run when the source pacakage is loaded and it needs to know to load all the actual code in the package
from app.source import source



