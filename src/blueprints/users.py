# Users Blueprint
from flask import Blueprint, jsonify

bp = Blueprint('users', __name__, url_prefix="/users")