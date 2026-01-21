# ADP Athlete Monitor Web Server
# Initialisation order:
# 0. System Imports
# 1. Load .env file
# 2. Logging
# 3. Celery
# 4. Database
# 5. Flask
# 6. Blueprints

# 0. System Imports
import sys, os
import time
from datetime import datetime as dt
import pytz as tz
import utils
from responses import Responses

# 1. Load .env file
import dotenv
if not dotenv.load_dotenv():
    print("[FATAL] Could not load .env file, exiting.")
    sys.exit(1)

# 2. Logging
import logging
log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=getattr(logging, log_level, logging.DEBUG),
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("Logging initialized at %s level", log_level)

# 3. Celery
import task_server as ts

# 4. Database
import psycopg2 as pg
logger.info("Initalising Database connection...")
logger.debug("Using DB username: %s, password: %s, host: %s, port: %s, dbname: %s", 
             os.getenv("DB_USER", "postgres"),
             os.getenv("DB_PASSWORD", "password"),
             os.getenv("DB_HOST", "localhost"),
             os.getenv("DB_PORT", "5432"),
             os.getenv("DB_NAME", "athletemonitor")
)
try:
    db_conn = pg.connect(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "athletemonitor")
    )
    db_conn.autocommit = True
except Exception as e:
    logger.fatal("Could not connect to Database: %s", e)
    sys.exit(1)

from db import Database
db = Database(db_conn)
db.database_table_constructor()
logger.info("Database connection established.")

# 5. Flask init
logger.info("Initalising Flask web server...")
from flask import Flask, jsonify
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/api'
app.config['APP_NAME'] = 'ADP Athlete Monitor'
app.config['VERSION'] = '0.0.1'
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY", "secret")
app.config['TZ_OBJ'] = tz.timezone(os.getenv("TZ", "UTC"))

from blueprints.auth import require_authentication, require_type, current_user, register

logger.info("Flask web server initialized.")

# 6. Blueprints
import blueprints as bp
import importlib

for module_name in bp.modules:
    try:
        module = importlib.import_module(f"blueprints.{module_name}")
        app.register_blueprint(module.bp)
        logger.debug("Registered blueprint: %s", module_name)
    except Exception as e:
        logger.error("Could not register blueprint %s: %s", module_name, e)
logger.info("All blueprints registered.")

# 7. Root routes (lol)
@app.route('/', methods=['GET'])
def index():
    return Responses.OK_200(data={
        "version": app.config['VERSION'],
        "status": "running",
        "timestamp": dt.now(tz.utc).isoformat()
    }).build()

@app.errorhandler(404)
def not_found(e):
    return Responses.Not_Found_404().build()

@app.errorhandler(500)
def internal_error(e):
    return Responses.Internal_Server_Error_500(details=str(e)).build()

@app.route('/response_test/<int:response_code>', methods=['GET'])
def response_test(response_code):
    return Responses.get(response_code).build()

if __name__ == '__main__':
    logger.info("Checking for admin user...")
    try:
        admin_user = db.execute_query_fetchall("SELECT id FROM users WHERE username = %s", ('admin',))[0]
        logger.info("Admin user found with ID: %s", admin_user[0])
    except IndexError:
        logger.warning("No admin user found, creating default admin user with username 'admin' and password 'adminpass'. Please change this password immediately after first login.")
        resp, status = register(
            username='admin',
            password=app.config.get("SECRET_KEY"),
            pname='Admin',
            fname='Default',
            lname='Administrator',
            email='admin@localhost',
            type='admin'
        )
        if status == 201:
            logger.info("Default admin user created successfully.")
        else:
            logger.fatal("Could not create default admin user: %s", resp.get("details"))
            sys.exit(1)

    logger.info("Starting Flask web server on %s:%s...", os.environ.get("APP_HOST", "0.0.0.0"), os.environ.get("APP_PORT", "8080"))
    app.run(host=os.environ.get("APP_HOST", "0.0.0.0"), port=int(os.environ.get("APP_PORT", 8080)), debug=(log_level == "DEBUG"))