import logging.config
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT: str = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

RABBIT_MQ_HOST: str = str(os.environ.get("RABBIT_MQ_HOST", "localhost"))
RABBIT_MQ_PORT: int = int(os.environ.get("RABBIT_MQ_PORT", "5672"))
RABBIT_MQ_USERNAME: str = str(os.environ.get("RABBIT_MQ_USERNAME", "guest"))
RABBIT_MQ_PASSWORD: str = str(os.environ.get("RABBIT_MQ_PASSWORD", "guest"))

NOTIFICATION_2_QUEUE_NAME = "nagp.order.queue.notification2"

EXCHANGE_INFO = {
    "order_place": {
        "exchange_name": "create_order_fanout",
        "exchange_type": "fanout",
        "routing_key": "order_created_routing_key",
        "event_name": "order_created",
    },
    "order_update": {
        "exchange_name": "update_order_topic",
        "exchange_type": "topic",
        "routing_key": "order_updated_routing_key",
        "event_name": "order_updated",
    },
}


LOG_DIR = os.environ.get("BACKEND_LOG_DIR", BASE_DIR)

LOG_LEVEL = bool(os.environ.get("LOG_LEVEL", "DEBUG"))
# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s" "%(message)s",
        }
    },
    "handlers": {
        "notification-service-2-log": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "notification_2_service.log"),
            "formatter": "json",
            "maxBytes": 1024 * 1024 * 200,
            "backupCount": 5,
        },
        "default": {
            "level": "DEBUG",
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "notification-service-2": {
            "handlers": ["default", "notification-service-2-log"],
            "level": LOG_LEVEL,
            "propagate": True,
        }
    },
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger("notification-service-2")
