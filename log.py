


import logging as l
import os
import subprocess
import sys
from logging.handlers import RotatingFileHandler


# Logger Variables
PYUPDATERLOGLEVEL = 35

def reset_logging():
    manager = l.root.manager
    manager.disabled = l.NOTSET
    for logger in manager.loggerDict.values():
        if isinstance(logger, l.Logger):
            logger.setLevel(l.NOTSET)
            logger.propagate = True
            logger.disabled = False
            logger.filters.clear()
            handlers = logger.handlers.copy()
            for handler in handlers:
                # Copied from `logging.shutdown`.
                try:
                    handler.acquire()
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    pass
                finally:
                    handler.release()
                logger.removeHandler(handler)






def setup_logging(loglevel):
    # Create a custom logging level to virtual pyupdater progress
    reset_logging()

    console_loglevel = loglevel or l.WARNING
    console_logformat = "[%(levelname)-8s] %(name)-30s : %(message)s"

    file_loglevel = l.INFO
    file_logformat = "%(asctime)-8s %(name)-30s %(levelname)-8s %(message)s"

    root_logger = l.getLogger()

    file_handler = RotatingFileHandler(
        #config_helpers.get_log_file_location(config_dir),
        "log.log",
        mode="a",  # append
        maxBytes=0.5 * 1000 * 1000,  # 512kB
        encoding="utf8",
        backupCount=5,  # once it hits 2.5MB total, start removing logs.
    )
    file_handler.setLevel(file_loglevel)  # set loglevel
    file_formatter = l.Formatter(
        file_logformat
    )  # a simple log file format
    file_handler.setFormatter(
        file_formatter
    )  # tell the file_handler to use this format

    console_handler = l.StreamHandler()
    console_handler.setLevel(console_loglevel)  # set loglevel
    console_formatter = l.Formatter(
        console_logformat
    )  # a simple console format
    console_handler.setFormatter(
        console_formatter
    )  # tell the console_handler to use this format

    # add the handlers to the root logger
    root_logger.setLevel(l.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    l.addLevelName(PYUPDATERLOGLEVEL, "Updater")

    # Suppress some of the overly verbose logs
    l.getLogger("sacn").setLevel(l.WARNING)
    l.getLogger("aiohttp.access").setLevel(l.WARNING)
    l.getLogger("pyupdater").setLevel(l.WARNING)
    l.getLogger("zeroconf").setLevel(l.WARNING)

    global _LOGGER
    _LOGGER = l.getLogger(__name__)


