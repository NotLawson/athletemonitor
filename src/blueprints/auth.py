# Auth Blueprint
#
# Overview:
# - User authentication
# - Token management
# - User registration

from flask import Blueprint, jsonify, request
import jwt
import hashlib, os, hmac
from datetime import datetime, timedelta, timezone
from __main__ import db, app, Responses
import logging
import psycopg2

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix="/auth")

# Directly from https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
def hash_new_password(password: str) -> tuple[bytes, bytes]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, pw_hash

def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    )


# Base functions
def authorize(username, password):
    # Dummy check for example purposes
    if username == 'example' and password == 'example':
        token = jwt.encode({'user': username, "exp": (datetime.now(timezone.utc) - timedelta(days=30)).timestamp()}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"token": token}), 200
    logger.debug("Authorizing user: %s with password %s", username, password)
    try:
        user = db.execute_query_fetchall(
            "SELECT id, password_salt, password_hash FROM users WHERE username = %s",
            (username,)
        )[0]
        id, salt, pw_hash = user
        if is_correct_password(bytes.fromhex(salt), bytes.fromhex(pw_hash), password):
            token = jwt.encode({'user': id, "exp": (datetime.now(timezone.utc) + timedelta(days=30)).timestamp()}, app.config['SECRET_KEY'], algorithm='HS256')
            return {"token": token}, 200
        logger.warning("Incorrect password for user: %s", username)
    except IndexError:
        # user not in database
        logger.warning("User not found: %s", username)
    return {"details": "Invalid username or password"}, 401

def current_user(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    auth_response, status_code = authenticate(token)
    if status_code != 200:
        return None
    return auth_response['user']

def authenticate(token):
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if decoded["exp"] < datetime.now(timezone.utc).timestamp():
            raise jwt.ExpiredSignatureError
        return {"user": decoded['user']}, 200
    except jwt.ExpiredSignatureError:
        return {"details": "Token has expired"}, 401
    except jwt.InvalidTokenError:
        return {"details": "Invalid token"}, 401

def register(username, password, pname, fname, lname, email, type):
    salt, pw_hash = hash_new_password(password)
    try:
        db.execute_query(
            "INSERT INTO users (username, email, password_hash, password_salt, pname, fname, lname, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (username, email, pw_hash.hex(), salt.hex(), pname, fname, lname, type)
        )
        return {"message": "User registered successfully"}, 201
    except psycopg2.IntegrityError as e:
        logger.warning("Registration failed for user %s: %s", username, e)
        return {"details": "Username or email already exists"}, 400
    except Exception as e:
        return {"details": str(e)}, 500

@bp.post('/authorize')
def route_authorize():
    username = request.json.get('username')
    password = request.json.get('password')
    response, status_code = authorize(username, password)

    match status_code:
        case 200:
            return Responses.OK_200(response).build()
        case 401:
            return Responses.Unauthorized_401(details=response.get("details")).build()
        case _:
            return Responses.Internal_Server_Error_500(details="An unknown error occurred during authorization.").build

@bp.get('/authenticate')
def route_authenticate():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    response, status_code = authenticate(token)

    match status_code:
        case 200:
            return Responses.OK_200(response).build() 
        case 401:
            return Responses.Unauthorized_401(details=response.get("details")).build()
        case _:
            return Responses.Internal_Server_Error_500(details="An unknown error occurred during authentication.").build()
    
@bp.post('/register')
def route_register():
    username = request.json.get('username')
    password = request.json.get('password')
    pname = request.json.get('fname') # set the preferred name to the first name for now
    fname = request.json.get('fname')
    lname = request.json.get('lname')
    email = request.json.get('email')
    type = request.json.get('type', 'student')
    response, status_code = register(username, password, pname, fname, lname, email, type)

    match status_code:
        case 201:
            return Responses.Created_201(response).build()
        case 400:
            return Responses.Bad_Request_400(details=response.get("details")).build()
        case _:
            return Responses.Internal_Server_Error_500(details="An unknown error occurred during registration.").build()

    
# Decorators
from functools import wraps
def require_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        auth_response, status_code = authenticate(token)
        if status_code != 200:
            return Responses.Unauthorized_401(details=auth_response.get("details")).build()
        request.user = auth_response['user']
        return f(*args, **kwargs)
    return decorated_function

def require_type(user_type):
    # 1. Admin
    # 2. Staff
    # 3. Student

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            auth_response, status_code = authenticate(token)
            if status_code != 200:
                return jsonify(auth_response), status_code
            user_id = auth_response['user']
            user = db.execute_query_fetchall(
                "SELECT type FROM users WHERE id = %s",
                (user_id,)
            )[0]
            match user_type:
                case 'admin':
                    if user[0] != 'admin':
                        return Responses.Forbidden_403(details="Insufficient permissions").build()
                case 'staff':
                    if user[0] not in ('admin', 'staff'):
                        return Responses.Forbidden_403(details="Insufficient permissions").build()
                case 'student':
                    if user[0] != 'student':
                        return Responses.Forbidden_403(details="Insufficient permissions").build()
            request.user = user_id
            return f(*args, **kwargs)
        return decorated_function
    return decorator

