# File: log_namager.py in backend
# Contains:
# - Logger class
# - Related settings

import os
import time
import logging
import threading

pattern = '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s'
folder = os.path.join(os.path.dirname(__file__), 'Logs')


class Logger(object):
    _instance_lock = threading.Lock()

    def __init__(self, folder=folder, name='Backend', level=logging.INFO):
        # Local logger,
        # Print INFO on terminal,
        # Write DEBUG on file.
        # - folder: Folder of the log file
        # - name: Name of the log
        # - level: Log level of terminal output

        if hasattr(self, 'logger'):
            self.logger.debug(
                'Singleton mode is used, ignore multiple import.')
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(pattern)
        self.level = level

        self.path = os.path.join(folder,
                                 '{}.log'.format(time.strftime('%Y%m%d%H%M%S')))
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except:
                pass

        # Setup handlers
        self.setup()

        print('=======================================')

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def setup(self):
        # Setup handlers for logger
        handlers = []

        # Setup stream handler
        stream = logging.StreamHandler()
        stream.setLevel(self.level)
        handlers.append(stream)

        # Setup file handler
        if self.path is not None:
            file = logging.FileHandler(self.path)
            file.setLevel(logging.DEBUG)
            handlers.append(file)

        # Setup format for handlers
        # Link handler with logger
        for h in handlers:
            h.setFormatter(self.formatter)
            self.logger.addHandler(h)
