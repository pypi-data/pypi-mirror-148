import logging
import logging_loki
from multiprocessing import Queue

class LoggerBroConfig():
    app_name: str
    """
    The app name to be added in the logs.
    """
    env = 'dev'
    loki_url: str
    """
    The url of the loki instance to send the logs to. 
    The default looks like this: `/loki/api/v1/push`
    """
    version: str
    """
    The version of the app. Will be part of the logs.
    """

    def __init__(self, *, app_name, loki_url, version, env) -> None:
        self.app_name = app_name
        self.loki_url = loki_url
        self.version = version
        self.env = env


def init_logger(config: LoggerBroConfig):
    for prop in ["app_name", "env", "loki_url", "version"]:
        if getattr(config, prop) is None:
            raise ValueError(f"Missing config property: {prop}")

    handler = logging_loki.LokiQueueHandler(
        Queue(-1),
        url=config.loki_url,
        # TODO: Create versioning for the logger. We need different logs
        # for v1 and v2
        tags={"application": config.app_name, "version": config.version},
        # Version is used internally by the client. It is irrelevant
        # to the api version
        version="1",
    )

    logger = logging.getLogger("loki")
    logger.addHandler(handler)
    logger.setLevel(level=logging.INFO)


def get_loki_logger():
    return logging.getLogger("loki")


def log_exception(exc: Exception):
    logger = get_loki_logger()
    logger.exception(
        exc, extra={"tags": {"level": logging.getLevelName(logging.ERROR)},},
    )
