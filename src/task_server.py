# ADP Monitor Task Runner
# Initialisation order:
# 0. System Imports
# 1. Load .env file
# 2. Logging
# 3. Celery
# 4. Database
# 5. Task Definitions
# 6. Celery Startup

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
from celery import Celery
logger.info("Initalising Celery...")
logger.debug("Using broker URL: %s", os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
try:
    celery = Celery("task_server", broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
except Exception as e:
    logger.fatal("Could not initialize Celery: %s", e)
    sys.exit(1)

# 4. Database
if __name__ == '__main__':
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

# 5. Task Definitions
@celery.task()
def example_task(x, y):
    logger.debug("Executing example_task with args: %s, %s", x, y)
    time.sleep(5)  # Simulate a long-running task
    result = x + y
    logger.debug("example_task result: %s", result)
    return result

# 6. Celery Startup
if __name__ == '__main__':
    logger.info("Starting Celery worker...")
    celery.start(['worker', '--loglevel=%s' % log_level.lower()])