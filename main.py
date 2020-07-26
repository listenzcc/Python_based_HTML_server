import time
import set_path

from logger import Logger

logger = Logger(name='PHB', path='logger.log').logger

if __name__ == '__main__':
    print('Python_based HTML backend starts.')
    print(time.ctime())
    print('Bye Bye.')

    logger.debug('logger debug message')
    logger.info('logger info message')
    logger.warning('logger warning message')
    logger.error('logger error message')
    logger.critical('logger critical message')
