# Stats Blueprint
#
# Overview:
# - Individuals Performance Stats
# - Group Performance Stats
# - Data Export
# - Streaks
# - School-wide stats
# - Upload stats

# IMPORTANT: This file will remain WIP until everything else is implemented.

from flask import Blueprint, jsonify, request
import datetime as dt
from __main__ import db, app, require_authentication, require_type, Responses, current_user

bp = Blueprint('stats', __name__, url_prefix="/stats")

# Individual Stats
@bp.get('/individual/daily/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_individual_daily_stats(user_id):
    '''
    Retrieve daily performance stats for a specific user.
    '''
    if request.mimetype == 'application/json':
        try: 
            date = request.json["date"]
            assert isinstance(date, str) and len(date.split('-')) == 3 and len(date.split('-')[0]) == 4 and len(date.split('-')[1]) == 2 and len(date.split('-')[2]) == 2
        except KeyError: date = (dt.datetime.now(tz=app.config['TZ_OBJ']) - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        except AssertionError: return Responses.Bad_Request_400(details="Date must be in YYYY-MM-DD format").build()
    else: date = (dt.datetime.now(tz=app.config['TZ_OBJ']) - dt.timedelta(days=1)).strftime('%Y-%m-%d')

    try: daily_log = db.execute_query_fetchall("SELECT id, timestamp, updated, daily_sleep_quality, daily_muscle_soreness, daily_mood, daily_stress_level, notes FROM log WHERE user_id = %s AND DATE(timestamp) = %s AND type = 'daily'",(user_id, date))[0]
    except IndexError: return Responses.Not_Found_404(details="No daily log found").build()

    return Responses.OK_200(data={
        "id": daily_log[0],
        "timestamp": daily_log[1],
        "updated": daily_log[2],
        "daily_sleep_quality": daily_log[3],
        "daily_muscle_soreness": daily_log[4],
        "daily_mood": daily_log[5],
        "daily_stress_level": daily_log[6],
        "notes": daily_log[7]
    }).build()

@bp.get('/individual/weekly/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_individual_weekly_stats(user_id):
    '''
    Retrieve weekly performance stats for a specific user.
    '''
    # TODO: Implement function
    pass

@bp.get('/individual/monthly/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_individual_monthly_stats(user_id):
    '''
    Retrieve monthly performance stats for a specific user.
    '''
    # TODO: Implement function
    pass

@bp.get('/individual/lifetime/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_individual_lifetime_stats(user_id):
    '''
    Retrieve lifetime performance stats for a specific user.
    '''
    try: user = db.execute_query_fetchall("SELECT id FROM users WHERE id = %s", (user_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="User not found").build

    logs = db.execute_query_fetchall("SELECT id, timestamp, updated, daily_sleep_quality, daily_muscle_soreness, daily_mood, daily_stress_level, notes FROM log WHERE user_id = %s AND type = 'daily' ORDER BY timestamp ASC",(user_id,))
    try: logs[0]
    except IndexError: return Responses.Not_Found_404(details="No logs found for user").build()

    stats = {
        "user_id": user_id,
        "logs": len(logs),
        "daily_sleep_quality": {
            "average": sum(log[3] for log in logs if log[3] is not None) / len([log for log in logs if log[3] is not None]),
            "min": min(log[3] for log in logs if log[3] is not None),
            "max": max(log[3] for log in logs if log[3] is not None),
            "median": sorted([log[3] for log in logs if log[3] is not None])[len([log for log in logs if log[3] is not None]) // 2]
        },
        "daily_muscle_soreness": {
            "average": sum(log[4] for log in logs if log[4] is not None) / len([log for log in logs if log[4] is not None]),
            "min": min(log[4] for log in logs if log[4] is not None),
            "max": max(log[4] for log in logs if log[4] is not None),
            "median": sorted([log[4] for log in logs if log[4] is not None])[len([log for log in logs if log[4] is not None]) // 2]
        },
        "daily_mood": {
            "average": sum(log[5] for log in logs if log[5] is not None) / len([log for log in logs if log[5] is not None]),
            "min": min(log[5] for log in logs if log[5] is not None),
            "max": max(log[5] for log in logs if log[5] is not None),
            "median": sorted([log[5] for log in logs if log[5] is not None])[len([log for log in logs if log[5] is not None]) // 2]
        },
        "daily_stress_level": {
            "average": sum(log[6] for log in logs if log[6] is not None) / len([log for log in logs if log[6] is not None]),
            "min": min(log[6] for log in logs if log[6] is not None),
            "max": max(log[6] for log in logs if log[6] is not None),
            "median": sorted([log[6] for log in logs if log[6] is not None])[len([log for log in logs if log[6] is not None]) // 2]
        }
    }

# My Stats
@bp.get('/individual/daily/me')
@require_authentication
def get_my_daily_stats():
    '''
    Retrieve daily performance stats for the authenticated user.
    '''
    user_id = current_user()
    if request.mimetype == 'application/json':
        try: 
            date = request.json["date"]
            assert isinstance(date, str) and len(date.split('-')) == 3 and len(date.split('-')[0]) == 4 and len(date.split('-')[1]) == 2 and len(date.split('-')[2]) == 2
        except KeyError: date = (dt.datetime.now(tz=app.config['TZ_OBJ']) - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        except AssertionError: return Responses.Bad_Request_400(details="Date must be in YYYY-MM-DD format").build()
    else: date = (dt.datetime.now(tz=app.config['TZ_OBJ']) - dt.timedelta(days=1)).strftime('%Y-%m-%d')

    try: daily_log = db.execute_query_fetchall("SELECT id, timestamp, updated, daily_sleep_quality, daily_muscle_soreness, daily_mood, daily_stress_level, notes FROM log WHERE user_id = %s AND DATE(timestamp) = %s AND type = 'daily'",(user_id, date))[0]
    except IndexError: return Responses.Not_Found_404(details="No daily log found").build()

    return Responses.OK_200(data={
        "id": daily_log[0],
        "timestamp": daily_log[1],
        "updated": daily_log[2],
        "daily_sleep_quality": daily_log[3],
        "daily_muscle_soreness": daily_log[4],
        "daily_mood": daily_log[5],
        "daily_stress_level": daily_log[6],
        "notes": daily_log[7]
    }).build()


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