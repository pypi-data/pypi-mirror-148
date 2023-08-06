# NewRelic Logger

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "inline image")

A simple project to log data to [NewRelic](https://newrelic.com/) using its [headerless logging api](https://docs.newrelic.com/docs/logs/log-api/introduction-log-api) along with [built-in logging](https://docs.python.org/3/library/logging.html).

The project was intended to send logs to both original monitoring tool and [NewRelic](https://newrelic.com/)


## Installing

```sh
pip install new_relic_logger
```

## Usage example

```sh
import logging
from new_relic_logger import NewRelicLogger

...
logger = NewRelicLogger(
    api_key=<API_KEY_HERE>,
    hostname=<HOST_NAME_HERE>,
    service=<SERVICE>,
    enable_built_in_logging=True,
)

logger.info("Updated User Object!")
...
logger.warning("Primary key for user object is not set yet!")
...
logger.error("Failed to retrive user profile!")
```
