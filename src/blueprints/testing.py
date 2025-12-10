# Testing Blueprint
from flask import Blueprint, jsonify

bp = Blueprint('testing', __name__, url_prefix="/testing")

@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200