import logging.handlers
import os
from datetime import datetime

import jdatetime


class CustomLogger(logging.Logger):
    def __init__(self, logger_name, level="DEBUG"):
        super().__init__(logger_name)
        self.setLevel(level)
        self.container_name = "container_name_test"
        self.logger_name = logger_name

        filename = self.get_filename(logger_name)
        handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when="midnight")

        formatter = logging.Formatter(f'%(levelname)s ** {self.container_name} ** %(message)s')
        handler.setFormatter(formatter)

        self.addHandler(handler)

    def get_filename(self, logger_name):
        base_name = os.path.basename(logger_name)
        time = datetime.now()
        persian_date = jdatetime.date.fromgregorian(date=time)
        persian_date_str = persian_date.strftime('%Y-%m-%d')
        new_filename = f"{self.container_name}_{base_name}_{persian_date_str}.log"

        return os.path.join("logs", new_filename)
