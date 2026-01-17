# Stats Blueprint
#
# Overview:
# - Individuals Performance Stats
# - Group Performance Stats
# - Data Export
# - Streaks
# - School-wide stats
# - Upload stats

from flask import Blueprint, jsonify
from __main__ import db, app, require_authentication, require_type

bp = Blueprint('stats', __name__, url_prefix="/stats")

# Individual Stats
@bp.get('/individual/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_individual_stats(user_id):
    '''
    Retrieve performance stats for an individual user.
    '''
    pass

@bp.get('/individual/<int:user_id>/<field>')
@require_authentication
@require_type('teacher')
def get_individual_stats_field(user_id, field):
    '''
    Retrieve specific field performance stats for an individual user.
    '''
    pass

# My Stats
@bp.get('/individual/me')
@require_authentication
def get_my_individual_stats():
    '''
    Retrieve performance stats for the authenticated user.
    '''
    pass

@bp.get('/individual/me/<field>')
@require_authentication
def get_my_individual_stats_field(field):
    '''
    Retrieve specific field performance stats for the authenticated user.
    '''
    pass

# Group Stats
@bp.get('/group/<int:group_id>')
@require_authentication
@require_type('teacher')
def get_group_stats(group_id):
    '''
    Retrieve performance stats for a group.
    '''
    pass

@bp.get('/group/<int:group_id>/<field>')
@require_authentication
@require_type('teacher')
def get_group_stats_field(group_id, field):
    '''
    Retrieve specific field performance stats for a group.
    '''
    pass

# Org Stats
@bp.get('/org')
@require_authentication
# Available to all authenticated users
def get_org_stats():
    '''
    Retrieve organization-wide performance stats.
    '''
    pass

@bp.get('/org/<field>')
@require_authentication
# Available to all authenticated users
def get_org_stats_field(field):
    '''
    Retrieve specific field organization-wide performance stats.
    '''
    pass

# Data Export and Streaks
@bp.get('/export')
@require_authentication
@require_type('teacher')
def export_stats():
    '''
    Export stats data.
    '''
    pass

@bp.get('/streaks/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_user_streaks(user_id):
    '''
    Retrieve streaks for a user.
    '''
    pass

@bp.get('/streaks/me')
@require_authentication
def get_my_streaks():
    '''
    Retrieve streaks for the authenticated user.
    '''
    pass

# Streak Freeze
@bp.post('/streaks/freeze/user/<int:user_id>')
@require_authentication
@require_type('teacher')
def freeze_user_streak(user_id):
    '''
    Freeze streak for a user, either until specified date or indefinitely.
    '''
    pass

@bp.post('/streaks/freeze/group/<int:group_id>')
@require_authentication
@require_type('teacher')
def freeze_group_streak(group_id):
    '''
    Freeze streak for a group, either until specified date or indefinitely.
    '''
    pass

@bp.post('/streaks/freeze/deepfreeze')
@require_authentication
@require_type('admin')
def freeze_org_streak():
    '''
    Freeze streak for the entire organization, either until specified date or indefinitely.
    '''
    pass

# Admin Stats Management
@bp.delete('/reset/<int:user_id>')
@require_authentication
@require_type('admin')
def reset_user_stats(user_id):
    '''
    Reset stats for a user.
    '''
    pass