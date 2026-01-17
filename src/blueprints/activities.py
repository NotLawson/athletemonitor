# Activities Blueprint
#
# Overview:
# - Activities management
# - Schedule management

from flask import Blueprint, jsonify, request
from __main__ import db, app, require_authentication, require_type

bp = Blueprint('activities', __name__, url_prefix="/activities")


# Schedule Endpoints
@bp.get('/schedule/<int:schedule_id>')
@require_authentication
def get_schedule(schedule_id):
    '''
    Retrieve a schedule by its ID.
    '''
    pass

@bp.patch('/schedule/<int:schedule_id>')
@require_authentication
def patch_schedule(schedule_id):
    '''
    Update a schedule by its ID.
    '''
    pass

@bp.delete('/schedule/<int:schedule_id>')
@require_authentication
def delete_schedule(schedule_id):
    '''
    Delete a schedule by its ID.
    '''
    pass

@bp.put('/schedule')
@require_authentication
def put_schedule():
    '''
    Create a new schedule.
    '''
    pass

@bp.get('/schedule/user/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_user_schedules(user_id):
    '''
    Retrieve all schedules for a specific user.
    '''
    pass

@bp.get('/schedule/me')
@require_authentication
def get_my_schedules():
    '''
    Retrieve all schedules for the authenticated user.
    '''
    pass

# Activity Endpoints
@bp.get('/activity/<int:activity_id>')
@require_authentication
def get_activity(activity_id):
    '''
    Retrieve an activity by its ID.
    '''
    pass

@bp.patch('/activity/<int:activity_id>')
@require_authentication
def patch_activity(activity_id):
    '''
    Update an activity by its ID.
    '''
    pass

@bp.delete('/activity/<int:activity_id>')
@require_authentication
def delete_activity(activity_id):
    '''
    Delete an activity by its ID.
    '''
    pass

@bp.put('/activity')
@require_authentication
def put_activity():
    '''
    Create a new activity.
    '''
    pass

@bp.get('/activity/schedule/<int:schedule_id>')
@require_authentication
def get_activities_by_schedule(schedule_id):
    '''
    Retrieve all activities for a specific schedule. (requires teacher or schedule owner)
    '''
    pass

@bp.get('/activity/user/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_activities_by_user(user_id):
    '''
    Retrieve all activities for a specific user.
    '''
    pass

@bp.get('/activity/me')
@require_authentication
def get_my_activities():
    '''
    Retrieve all activities for the authenticated user.
    '''
    pass
