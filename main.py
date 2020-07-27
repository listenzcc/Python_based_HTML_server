import time
from local_toolbox import Server, Logger


logger = Logger(name='PHB', path='logger.log').logger

server = Server(logger=logger)

if __name__ == '__main__':
    print('Python_based HTML backend starts.')
    print(time.ctime())

    server.start()

    while True:
        if input('>> ') == 'q':
            server.running = False
            break

    print('Bye Bye.')

    # logger.debug('logger debug message')
    # logger.info('logger info message')
    # logger.warning('logger warning message')
    # logger.error('logger error message')
    # logger.critical('logger critical message')
