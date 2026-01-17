# Admin Blueprint
#
# Overview:
# - All Admin endpoints

from flask import Blueprint, jsonify
from __main__ import db, app, require_authentication, require_type
bp = Blueprint('admin', __name__, url_prefix="/admin")

@bp.get('/sync/users')
@require_authentication
@require_type('admin')
def sync_users():
    '''
    Sync users from external system.
    '''
    pass