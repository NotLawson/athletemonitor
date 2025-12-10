# Logs Blueprint
from flask import Blueprint, jsonify

bp = Blueprint('logs', __name__, url_prefix="/logs")