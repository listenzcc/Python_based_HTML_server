import logging

pattern = '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s'


class Logger():
    def __init__(self, path=None, name='root', level=logging.INFO):
        # Local logger
        # path: Full path of logging file
        # name: Name of the log
        # level: Log level of terminal output

        # Settings
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(pattern)
        self.path = path
        self.level = level

        # Setup handlers
        self.setup()

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
