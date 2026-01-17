# Identity Blueprint
#
# Overview:
# - User details
# - User management
# - Group management

from flask import Blueprint, jsonify, request
from __main__ import db, app, require_authentication, require_type, current_user, Responses, register


bp = Blueprint('iden', __name__, url_prefix="/iden")

# Users
@bp.get('/user')
@require_authentication
@require_type('admin')
def get_all_users():
    '''
    Retrieve a list of all users.
    '''
    limit: int = request.json.get('limit', 100)
    try: assert isinstance(limit, int) and limit > 0 and limit <= 1000
    except AssertionError: return Responses.Bad_Request_400(details="Invalid limit").build()

    sort_by: str = request.json.get('sort_by', 'id')
    try: assert sort_by in ['id', 'username', 'created_at', 'last_login']
    except AssertionError: return Responses.Bad_Request_400(details="Invalid sort_by").build()

    sort_order: str = request.json.get('sort_order', 'asc')
    try: assert sort_order in ['asc', 'desc']
    except AssertionError: return Responses.Bad_Request_400(details="Invalid sort_order").build()


    users = db.execute_query_fetchall("SELECT id, username, pname, fname, lname, email, groups, type, ftue_complete, created_at, last_login FROM users ORDER BY {} {} LIMIT %s".format(sort_by, sort_order), (limit,))
    return Responses.OK_200(data={"users": users}).build()

@bp.get('/user/<int:user_id>')
@require_authentication
@require_type('teacher')
def get_user_details(user_id):
    '''
    Retrieve user details by user ID.
    '''
    try: user = db.execute_query_fetchall("SELECT id, username, pname, fname, lname, email, groups, type, ftue_complete, created_at, last_login FROM users WHERE id = %s", (user_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="User not found").build()
    return Responses.OK_200(data={"user": user}).build()

@bp.patch('/user/<int:user_id>')
@require_authentication
@require_type('teacher')
def update_user_details(user_id):
    '''
    Update user details by user ID.
    '''
    try: user = db.execute_query_fetchall("SELECT id FROM users WHERE id = %s", (user_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="User not found").build()
    
    db.execute_query("UPDATE users SET username = %s, pname = %s, fname = %s, lname = %s, email = %s, groups = %s, type = %s, ftue_complete = %s WHERE id = %s", (
        request.json.get('username', user[0]),
        request.json.get('pname', user[1]),
        request.json.get('fname', user[2]),
        request.json.get('lname', user[3]),
        request.json.get('email', user[4]),
        request.json.get('groups', user[5]),
        request.json.get('type', user[6]),
        request.json.get('ftue_complete', user[7]),
        user_id
    ))

    return Responses.OK_200().build()

@bp.delete('/user/<int:user_id>')
@require_authentication
@require_type('admin')
def delete_user(user_id):
    '''
    Delete a user by user ID.
    '''
    try: db.execute_query_fetchall("SELECT id FROM users WHERE id = %s", (user_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="User not found").build()
    db.execute_query("DELETE FROM users WHERE id = %s", (user_id,))
    return Responses.OK_200().build()

@bp.post('/user')
@require_authentication
@require_type('admin')
def create_user():
    '''
    Create a new user.
    '''
    try:
        username = request.json['username']
        try: assert len(username) >= 3 and len(username) <= 20
        except AssertionError: return Responses.Bad_Request_400(details="Username must be between 3 and 20 characters").build()

        password = request.json['password']
        try: assert len(password) >= 8 and len(password) <= 25
        except AssertionError: return Responses.Bad_Request_400(details="Password must be between 8 and 25 characters").build()

        fname = request.json['fname']
        try: assert len(fname) >= 1 and len(fname) <= 30
        except AssertionError: return Responses.Bad_Request_400(details="First name must be between 1 and 30 characters").build()

        pname = request.json.get('pname', fname)
        try: assert len(pname) >= 1 and len(pname) <= 30
        except AssertionError: return Responses.Bad_Request_400(details="Preferred name must be between 1 and 30 characters").build()

        lname = request.json['lname']
        try: assert len(lname) >= 1 and len(lname) <= 30
        except AssertionError: return Responses.Bad_Request_400(details="Last name must be between 1 and 30 characters").build()

        email = request.json['email']
        try: assert "@" in email and len(email) <= 50
        except AssertionError: return Responses.Bad_Request_400(details="Invalid email address").build()

        groups = request.json.get('groups', [])
        try: assert isinstance(groups, list) and all(isinstance(g, int) for g in groups) and all(len(db.execute_query_fetchall("SELECT id FROM groups WHERE id = %s", (g,))) > 0 for g in groups)
        except AssertionError: return Responses.Bad_Request_400(details="One or more groups are invalid").build()

        type = request.json.get('type', 'student')
        try: assert type in ['student', 'teacher', 'admin']
        except AssertionError: return Responses.Bad_Request_400(details="Invalid user type").build()
    except KeyError as e:
        return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()
    
    resp = register(username, password, pname, fname, lname, email, type)
    match resp[1]:
        case 201:
            user_id = db.execute_query_fetchall("SELECT id FROM users WHERE username = %s", (username,))[0][0]
            for group_id in groups:
                join_group(user_id, group_id)
            return Responses.Created_201(data={"user_id": user_id}).build()
        case 400:
            return Responses.Bad_Request_400(details=resp[0].get("details")).build()
        case _:
            return Responses.Internal_Server_Error_500(details="An unknown error occurred during user creation.").build()
        
# Me endpoints
@bp.get('/user/me')
@require_authentication
def get_own_details():
    '''
    Retrieve details of the authenticated user.
    '''
    user = current_user(request)
    details = db.execute_query_fetchone("SELECT id, username, pname, fname, lname, email, groups, type, ftue_complete, created_at, last_login FROM users WHERE id = %s", (user,))
    return Responses.OK_200(data={"user": details}).build()

@bp.patch('/user/me')
@require_authentication
def update_own_details():
    '''
    Update details of the authenticated user.
    '''
    user = current_user(request)
    current_details = db.execute_query_fetchone("SELECT username, pname, fname, lname, email, type, ftue_complete FROM users WHERE id = %s", (user,))
    db.execute_query("UPDATE users SET username = %s, pname = %s, fname = %s, lname = %s, email = %s, type = %s, ftue_complete = %s WHERE id = %s", (
        request.json.get('username', current_details[0]),
        request.json.get('pname', current_details[1]),
        request.json.get('fname', current_details[2]),
        request.json.get('lname', current_details[3]),
        request.json.get('email', current_details[4]),
        request.json.get('type', current_details[5]),
        request.json.get('ftue_complete', current_details[6]),
        user
    ))
    return Responses.OK_200().build()

# Groups
def join_group(user_id, group_id):
    '''
    Add a user to a group.
    '''
    user = db.execute_query_fetchone("SELECT id, groups, type FROM users WHERE id = %s", (user_id,))
    if group_id in user[1]:
        return "User already in group", 400
    match user[2]:
        case 'student':
            db.execute_query("UPDATE users SET groups = array_append(groups, %s) WHERE id = %s", (group_id, user_id))
            db.execute_query("UPDATE groups SET students = array_append(students, %s) WHERE id = %s", (user_id, group_id))
        case 'teacher' | 'admin':
            db.execute_query("UPDATE users SET groups = array_append(groups, %s) WHERE id = %s", (group_id, user_id))
            db.execute_query("UPDATE groups SET staff = array_append(staff, %s) WHERE id = %s", (user_id, group_id))
        case _:
            return "Invalid user type", 500
    return "User added to group", 200
    
def leave_group(user_id, group_id):
    '''
    Remove a user from a group.
    '''
    user = db.execute_query_fetchone("SELECT id, groups, type FROM users WHERE id = %s", (user_id,))
    if group_id not in user[1]:
        return "User not in group", 400
    match user[2]:
        case 'student':
            db.execute_query("UPDATE users SET groups = array_remove(groups, %s) WHERE id = %s", (group_id, user_id))
            db.execute_query("UPDATE groups SET students = array_remove(students, %s) WHERE id = %s", (user_id, group_id))
        case 'teacher' | 'admin':
            db.execute_query("UPDATE users SET groups = array_remove(groups, %s) WHERE id = %s", (group_id, user_id))
            db.execute_query("UPDATE groups SET staff = array_remove(staff, %s) WHERE id = %s", (user_id, group_id))
        case _:
            return "Invalid user type", 500
    return "User removed from group", 200

@bp.get('/groups')
@require_authentication
@require_type('teacher')
def get_all_groups():
    '''
    Retrieve a list of all groups.
    '''
    groups = db.execute_query_fetchall("SELECT id, name, description, created_at, staff, students FROM groups")
    return Responses.OK_200(data={"groups": groups}).build()

@bp.put('/group')
@require_authentication
@require_type('admin')
def create_group():
    '''
    Create a new group.
    '''
    try:
        name = request.json['name']
        try: assert len(name) >= 3 and len(name) <= 50
        except AssertionError: return Responses.Bad_Request_400(details="Group name must be between 3 and 50 characters").build()

        description = request.json.get('description', '')
        try: assert len(description) <= 255
        except AssertionError: return Responses.Bad_Request_400(details="Group description must be less than 255 characters").build()

        short = request.json['short']
        try: assert len(short) >= 2 and len(short) <= 10
        except AssertionError: return Responses.Bad_Request_400(details="Group short name must be between 2 and 10 characters").build()

        type = request.json['type']
        try: assert type in ['class', 'team', 'grade', 'org']
        except AssertionError: return Responses.Bad_Request_400(details="Invalid group type").build()
        
        staff = request.json.get('staff', [current_user(request)])
        try: assert isinstance(staff, list) and all(isinstance(s, int) for s in staff) and all(len(db.execute_query_fetchall("SELECT id FROM users WHERE id = %s AND type IN ('teacher', 'admin')", (s,))) > 0 for s in staff)
        except AssertionError: return Responses.Bad_Request_400(details="One or more staff members are invalid").build()

        students = request.json.get('students', [])
        try: assert isinstance(students, list) and all(isinstance(s, int) for s in students) and all(len(db.execute_query_fetchall("SELECT id FROM users WHERE id = %s AND type = 'student'", (s,))) > 0 for s in students)
        except AssertionError: return Responses.Bad_Request_400(details="One or more students are invalid").build()

        db.execute_query("INSERT INTO groups (name, description, short, type) VALUES (%s, %s, %s, %s)", (
            name,
            description,
            short,
            type,
        ))
        for staff_id in staff:
            join_group(staff_id, db.execute_query_fetchall("SELECT id FROM groups WHERE name = %s AND short = %s", (name, short))[0][0])
        for student_id in students:
            join_group(student_id, db.execute_query_fetchall("SELECT id FROM groups WHERE name = %s AND short = %s", (name, short))[0][0])
        
        return Responses.Created_201().build()
    except KeyError as e:
        return Responses.Bad_Request_400(details=f"Missing required field: {e.args[0]}").build()

@bp.get('/group/<int:group_id>')
@require_authentication
def get_group_details(group_id):
    '''
    Retrieve group details by group ID.
    '''
    try: group = db.execute_query_fetchall("SELECT id, name, description, short, type, created_at FROM groups WHERE id = %s", (group_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="Group not found").build()
    return Responses.OK_200(data={"group": group}).build()

@bp.patch('/group/<int:group_id>')
@require_authentication
@require_type('admin')
def update_group(group_id):
    '''
    Update group details by group ID.
    '''
    try: group = db.execute_query_fetchall("SELECT id, name, description, short, type FROM groups WHERE id = %s", (group_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="Group not found").build()
    db.execute_query("UPDATE groups SET name = %s, description = %s, short = %s, type = %s WHERE id = %s", (
        request.json.get('name', group[1]),
        request.json.get('description', group[2]),
        request.json.get('short', group[3]),
        request.json.get('type', group[4]),
        group_id
    ))
    return Responses.OK_200().build()

@bp.delete('/group/<int:group_id>')
@require_authentication
@require_type('admin')
def delete_group(group_id):
    '''
    Delete a group by group ID.
    '''
    try: db.execute_query_fetchall("SELECT id FROM groups WHERE id = %s", (group_id,))[0]
    except IndexError: return Responses.Not_Found_404(details="Group not found").build()
    db.execute_query("DELETE FROM groups WHERE id = %s", (group_id,))
    return Responses.OK_200().build()

