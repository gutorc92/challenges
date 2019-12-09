"""
Gunicorn app to run API without debug flag as default
"""

from eve.io.mongo import MongoJSONEncoder
from api import app as application
# pylint: disable=wrong-import-order
import logging
# pylint: disable=invalid-name
gunicorn_logger = logging.getLogger('gunicorn.error')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    application.json_encoder = MongoJSONEncoder
    application.run()
