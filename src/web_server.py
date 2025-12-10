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

# 1. Load .env file
import dotenv
if not dotenv.load_dotenv("../.env"):
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
logger.info("Database connection established.")

# Flask init
logger.info("Initalising Flask web server...")
from flask import Flask, jsonify
app = Flask(__name__, root_path="/api")
app.config['APP_NAME'] = 'ADP Athlete Monitor'
app.config['VERSION'] = '0.0.1'
logger.info("Flask web server initialized.")

# 6. Blueprints
import blueprints as bp
import importlib

for module_name in bp.modules:
    logger.info("Registering blueprint: %s", module_name)
    try:
        module = importlib.import_module(f"blueprints.{module_name}")
        app.register_blueprint(module.bp)
        logger.info("Registered blueprint: %s", module_name)
    except Exception as e:
        logger.error("Could not register blueprint %s: %s", module_name, e)

