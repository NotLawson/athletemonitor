# Logs Blueprint
#
# Overview:
# - Read, write, update and delete logs
# - Filter logs by user, date, type, etc.

from flask import Blueprint, jsonify, request
from __main__ import db, app, require_authentication, require_type, current_user, Responses

bp = Blueprint('logs', __name__, url_prefix="/logs")

@bp.get('/<int:log_id>')
@require_authentication
def get_log(log_id):
    '''
    Retrieve a log by its ID.
    '''
    try: metadata = db.execute_query_fetchall("SELECT type, user_id FROM log WHERE id = %s", (log_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="Log not found").build()
    user = current_user(request)
    if user != metadata[1]:
        return Responses.Forbidden_403(details="You do not have permission to view this log").build()
    match metadata[0]:
        case 'daily':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, daily_muscle_soreness, daily_mood, daily_stress_level, notes FROM log WHERE id = %s", (log_id,))
            return Responses.OK_200(data={
                "id": log_id,
                "user_id": log[0],
                "timestamp": log[1],
                "updated": log[2],
                "daily_muscle_soreness": log[3],
                "daily_mood": log[4],
                "daily_stress_level": log[5],
                "notes": log[6]
            }).build()
        
        case 'injury':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, injury_title, injury_state, injury_severity, notes FROM log WHERE id = %s", (log_id,))
            return Responses.OK_200(data={
                "id": log_id,
                "user_id": log[0],
                "timestamp": log[1],
                "updated": log[2],
                "injury_title": log[3],
                "injury_state": log[4],
                "injury_severity": log[5],
                "notes": log[6]
            }).build()
        
        case 'activity':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, activity_duration_minutes, activity_RPE, activity_related_id, notes FROM log WHERE id = %s", (log_id,))
            return Responses.OK_200(data={
                "id": log_id,
                "user_id": log[0],
                "timestamp": log[1],
                "updated": log[2],
                "activity_duration_minutes": log[3],
                "activity_RPE": log[4],
                "activity_related_id": log[5],
                "notes": log[6]
            }).build()

        case 'study':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, study_duration_minutes, notes FROM log WHERE id = %s", (log_id,))
            return Responses.OK_200(data={
                "id": log_id,
                "user_id": log[0],
                "timestamp": log[1],
                "updated": log[2],
                "study_duration_minutes": log[3],
                "notes": log[4]
            }).build()
        
        case 'sleep':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, sleep_quality, sleep_duration_minutes, notes FROM log WHERE id = %s", (log_id,))
            return Responses.OK_200(data={
                "id": log_id,
                "user_id": log[0],
                "timestamp": log[1],
                "updated": log[2],
                "sleep_quality": log[3],
                "sleep_duration_minutes": log[4],
                "notes": log[5]
            }).build()

        case _:
            return Responses.Internal_Server_Error_500(details="Unknown log type").build()

@bp.delete('/<int:log_id>')
@require_authentication
def delete_log(log_id):
    '''
    Delete a log by its ID.
    '''
    user = current_user(request)
    try: log_owner = db.execute_query_fetchall("SELECT user_id FROM log WHERE id = %s", (log_id,))[0][0]
    except IndexError: return Responses.Not_Found_404(details="Log not found").build()
    if user != log_owner:
        return Responses.Forbidden_403(details="You do not have permission to delete this log").build()
    else:
        db.execute_query("DELETE FROM log WHERE id = %s", (log_id,))
        return Responses.OK_200(data={"message": "Log deleted successfully"}).build()

@bp.patch('/<int:log_id>')
@require_authentication
def patch_log(log_id):
    '''
    Update a log by its ID.
    '''
    try: metadata = db.execute_query_fetchall("SELECT type FROM log WHERE id = %s", (log_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="Log not found").build()
    match metadata[0]:
        case 'daily':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, daily_muscle_soreness, daily_mood, daily_stress_level, notes FROM log WHERE id = %s", (log_id,))
            db.execute_query("UPDATE log SET daily_muscle_soreness = %s, daily_mood = %s, daily_stress_level = %s, notes = %s, updated = NOW() WHERE id = %s", (
                request.json.get('daily_muscle_soreness', log[3]),
                request.json.get('daily_mood', log[4]),
                request.json.get('daily_stress_level', log[5]),
                request.json.get('notes', log[6]),
                log_id
            ))
            return Responses.OK_200(data={"message": "Log updated successfully"}).build()
        
        case 'injury':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, injury_title, injury_state, injury_severity, notes FROM log WHERE id = %s", (log_id,))
            db.execute_query("UPDATE log SET injury_title = %s, injury_state = %s, injury_severity = %s, notes = %s, updated = NOW() WHERE id = %s", (
                request.json.get('injury_title', log[3]),
                request.json.get('injury_state', log[4]),
                request.json.get('injury_severity', log[5]),
                request.json.get('notes', log[6]),
                log_id
            ))
            return Responses.OK_200(data={"message": "Log updated successfully"}).build()
        
        case 'activity':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, activity_duration_minutes, activity_RPE, activity_related_id, notes FROM log WHERE id = %s", (log_id,))
            db.execute_query("UPDATE log SET activity_duration_minutes = %s, activity_RPE = %s, activity_related_id = %s, notes = %s, updated = NOW() WHERE id = %s", (
                request.json.get('activity_duration_minutes', log[3]),
                request.json.get('activity_RPE', log[4]),
                request.json.get('activity_related_id', log[5]),
                request.json.get('notes', log[6]),
                log_id
            ))
            return Responses.OK_200(data={"message": "Log updated successfully"}).build()
        
        case 'study':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, study_duration_minutes, notes FROM log WHERE id = %s", (log_id,))
            db.execute_query("UPDATE log SET study_duration_minutes = %s, notes = %s, updated = NOW() WHERE id = %s", (
                request.json.get('study_duration_minutes', log[3]),
                request.json.get('notes', log[4]),
                log_id
            ))
            return Responses.OK_200(data={"message": "Log updated successfully"}).build()

        case 'sleep':
            log = db.execute_query_fetchone("SELECT user_id, timestamp, updated, sleep_quality, sleep_duration_minutes, notes FROM log WHERE id = %s", (log_id,))
            db.execute_query("UPDATE log SET sleep_quality = %s, sleep_duration_minutes = %s, notes = %s, updated = NOW() WHERE id = %s", (
                request.json.get('sleep_quality', log[3]),
                request.json.get('sleep_duration_minutes', log[4]),
                request.json.get('notes', log[5]),
                log_id
            ))
            return Responses.OK_200(data={"message": "Log updated successfully"}).build()
        
        case _:
            return Responses.Internal_Server_Error_500(details="Unknown log type").build()

@bp.put('/')
@require_authentication
def put_log():
    '''
    Create a new log.
    '''
    user = current_user(request)

    try:
        log_type = request.json['type']
    except KeyError:
        return Responses.Bad_Request_400(details="Log type is required").build()
    
    match log_type:
        case 'daily':
            try:
                daily_muscle_soreness = request.json['daily_muscle_soreness']
                daily_mood = request.json['daily_mood']
                daily_stress_level = request.json['daily_stress_level']
                notes = request.json.get('notes', '')
            except KeyError as e:
                return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
            
            db.execute_query("INSERT INTO log (user_id, type, timestamp, updated, daily_muscle_soreness, daily_mood, daily_stress_level, notes) VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s)", (
                user,
                'daily',
                daily_muscle_soreness,
                daily_mood,
                daily_stress_level,
                notes
            ))
            return Responses.Created_201(data={"message": "Daily log created successfully"}).build()
        
        case 'injury':
            try:
                injury_title = request.json['injury_title']
                injury_state = request.json['injury_state']
                injury_severity = request.json['injury_severity']
                notes = request.json.get('notes', '')
            except KeyError as e:
                return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
            
            db.execute_query("INSERT INTO log (user_id, type, timestamp, updated, injury_title, injury_state, injury_severity, notes) VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s)", (
                user,
                'injury',
                injury_title,
                injury_state,
                injury_severity,
                notes
            ))
            return Responses.Created_201(data={"message": "Injury log created successfully"}).build()
        
        case 'activity':
            try:
                activity_duration_minutes = request.json['activity_duration_minutes']
                activity_RPE = request.json['activity_RPE']
                activity_related_id = request.json.get('activity_related_id', None)
                notes = request.json.get('notes', '')
            except KeyError as e:
                return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
            
            db.execute_query("INSERT INTO log (user_id, type, timestamp, updated, activity_duration_minutes, activity_RPE, activity_related_id, notes) VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s)", (
                user,
                'activity',
                activity_duration_minutes,
                activity_RPE,
                activity_related_id,
                notes
            ))
            return Responses.Created_201(data={"message": "Activity log created successfully"}).build()
        
        case 'study':
            try:
                study_duration_minutes = request.json['study_duration_minutes']
                notes = request.json.get('notes', '')
            except KeyError as e:
                return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
            
            db.execute_query("INSERT INTO log (user_id, type, timestamp, updated, study_duration_minutes, notes) VALUES (%s, %s, NOW(), NOW(), %s, %s)", (
                user,
                'study',
                study_duration_minutes,
                notes
            ))
            return Responses.Created_201(data={"message": "Study log created successfully"}).build()
        
        case 'sleep':
            try:
                sleep_quality = request.json['sleep_quality']
                sleep_duration_minutes = request.json['sleep_duration_minutes']
                notes = request.json.get('notes', '')
            except KeyError as e:
                return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
            db.execute_query("INSERT INTO log (user_id, type, timestamp, updated, sleep_quality, sleep_duration_minutes, notes) VALUES (%s, %s, NOW(), NOW(), %s, %s, %s)", (
                user,
                'sleep',
                sleep_quality,
                sleep_duration_minutes,
                notes
            ))
            return Responses.Created_201(data={"message": "Sleep log created successfully"}).build()

        case _:
            return Responses.Bad_Request_400(details="Invalid log type").build()

@bp.get('/')
@require_authentication
def filter_log():
    '''
    Filter logs based on query parameters.
    Example query parameters:
    - filter: user_id, date, log_type
    - limit: number of results
    - sort: asc/desc
    '''
    filter: str = request.json.get('filter', None)
    try: assert filter is None or (isinstance(filter, str) and filter in ['user_id', 'date', 'log_type'])
    except AssertionError: return Responses.Bad_Request_400(details="Invalid filter parameter").build()

    limit: int = request.json.get('limit', 100)
    try: assert isinstance(limit, int) and limit > 0
    except AssertionError: return Responses.Bad_Request_400(details="Invalid limit parameter, must be a positive integer").build()

    sort: str = request.json.get('sort', 'desc')
    try: assert sort in ['asc', 'desc']
    except AssertionError: return Responses.Bad_Request_400(details="Invalid sort parameter, must be 'asc' or 'desc'").build()
    
    match filter:
        case None:
            logs = db.execute_query_fetchall(f"SELECT * FROM log ORDER BY timestamp {sort.upper()} LIMIT %s", (limit,))
            return Responses.OK_200(data={"logs": logs}).build()
        case 'user_id':
            user_id: int = request.json.get('user_id', None)
            try: assert isinstance(user_id, int)
            except AssertionError: return Responses.Bad_Request_400(details="Invalid user_id parameter").build()

            logs = db.execute_query_fetchall(f"SELECT * FROM log WHERE user_id = %s ORDER BY timestamp {sort.upper()} LIMIT %s", (user_id, limit))
            return Responses.OK_200(data={"logs": logs}).build()
        case 'date':
            date: str = request.json.get('date', None)
            try: assert isinstance(date, str)
            except AssertionError: return Responses.Bad_Request_400(details="Invalid date parameter").build()

            logs = db.execute_query_fetchall(f"SELECT * FROM log WHERE DATE(timestamp) = %s ORDER BY timestamp {sort.upper()} LIMIT %s", (date, limit))
            return Responses.OK_200(data={"logs": logs}).build()
        case 'log_type':
            log_type: str = request.json.get('log_type', None)
            try: assert isinstance(log_type, str) and log_type in ['daily', 'injury', 'activity', 'study']
            except AssertionError: return Responses.Bad_Request_400(details="Invalid log_type parameter").build()

            logs = db.execute_query_fetchall(f"SELECT * FROM log WHERE type = %s ORDER BY timestamp {sort.upper()} LIMIT %s", (log_type, limit))
            return Responses.OK_200(data={"logs": logs}).build()
    pass