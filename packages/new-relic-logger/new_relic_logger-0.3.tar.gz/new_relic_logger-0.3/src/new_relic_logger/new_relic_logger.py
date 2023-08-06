"""
Centralize built-in loggina and new relic logging
"""
import logging
import requests


class NewRelicLogger:
    """
    Simple Python Wrapper for New Relic Logging.
    Log level would be helpful to filter logs by level
    and that can also easily replace current logging module
    """

    # constants for logging levels
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    # map logging levels to description string
    _levels_map = {
        NOTSET: "notset",
        DEBUG: "debug",
        INFO: "info",
        WARNING: "warning",
        ERROR: "error",
        CRITICAL: "critical"
    }

    _url = "https://log-api.newrelic.com/log/v1"
    _logger = None

    def __init__(
        self,
        api_key: str,
        hostname: str = 'Unknown',
        service: str = 'Unknown',
        headerless: bool = True,
        enable_built_in_logging: bool = True,
        log_level: int = logging.INFO,
    ):
        """
        Initialize logger
        """
        self.hostname = hostname
        self.service = service

        # api_key is required
        if not api_key:
            raise ValueError('Missing API Key')

        # headerless puts api key in url
        if headerless:
            self._url = f'{self._url}?Api-Key={api_key}'
            self.headers = None
        # embed api key to request headers
        else:
            self.headers = {
                'Content-Type': 'application/json',
                'Content-Encoding': 'gzip',
                'Api-Key': api_key
            }

        if enable_built_in_logging:
            self._logger = logging.getLogger(service)
            self._logger.setLevel(log_level)

        self.logging_level = log_level

    def log(self, msg: str, log_level: int = logging.INFO, *args, **kwargs):
        """
        Log the message
        """
        # compose data with NewRelic attributes and message
        data = {
            "service": self.service,
            "hostname": self.hostname,
            "log_level": self._levels_map[log_level],
            "message": msg
        }

        # log to built-in logging
        if self._logger:
            self._logger.log(level=log_level, msg=msg, *args, **kwargs)

        # send logs to new relic
        try:
            requests.post(self._url, json=data, headers=self.headers)
        except Exception as e:
            raise e

    def info(self, msg: str):
        self.log(msg, log_level=self.INFO)

    def debug(self, msg: str):
        self.log(msg, log_level=self.DEBUG)

    def warning(self, msg: str):
        self.log(msg, log_level=self.WARNING)

    def error(self, msg: str):
        self.log(msg, log_level=self.ERROR)

    def critical(self, msg: str):
        self.log(msg, log_level=self.CRITICAL)
