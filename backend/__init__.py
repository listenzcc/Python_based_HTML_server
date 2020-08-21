from . import log_manager
from . import http_bottom_server

logger = log_manager.Logger()
server = http_bottom_server.Server(logger=logger.logger)

logger.logger.debug('Backend is imported')
