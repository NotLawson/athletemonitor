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
from datetime import datetime as dt, timezone as tz
import utils

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

# Flask init
logger.info("Initalising Flask web server...")
from flask import Flask, jsonify
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/api'
app.config['APP_NAME'] = 'ADP Athlete Monitor'
app.config['VERSION'] = '0.0.1'
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
    return jsonify({
        "app_name": app.config['APP_NAME'],
        "version": app.config['VERSION'],
        "status": "running",
        "timestamp": dt.now(tz.utc).isoformat()
    }), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "details": str(e)}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Flask web server on %s:%s...", os.environ.get("APP_HOST", "0.0.0.0"), os.environ.get("APP_PORT", "8080"))
    app.run(host=os.environ.get("APP_HOST", "0.0.0.0"), port=int(os.environ.get("APP_PORT", 8080)), debug=(log_level == "DEBUG"))