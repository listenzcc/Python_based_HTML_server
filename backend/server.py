import socket
import urllib.parse
import threading


charset = 'utf-8'


def encode(src, encoding=charset):
    if isinstance(src, bytes):
        return src
    return src.encode(encoding)


def default_resp(request, charset=charset):
    # Default response method
    print('----------------------------------')
    print(request)
    print('==================================')

    # Set content as [request]
    content = encode(request)
    content_length = len(content)
    content_type = 'text/plain'

    # Header
    response = ['HTTP/1.1 200 OK',
                'Accept-Ranges: bytes',
                'ETag: W/"269-1482321927478"',
                'Content-Language: zh-CN']
    # Allow origin access
    response.append('Access-Control-Allow-Origin: *')
    # Content-Type
    response.append(f'Content-Type: {content_type}; charset={charset}')
    # Content-Length
    response.append(f'Content-Length: {content_length} \n')
    # Content
    response.append(content)

    return b'\n'.join([encode(e) for e in response])


class Server():
    def __init__(self, logger, resp=default_resp, IP='localhost', port=8612):
        # Initialize server
        # Running flag
        self.running = False

        # Customized logger instance
        self.logger = logger

        # Response method
        self.resp = resp

        # IP and port
        self.IP = IP
        self.port = port

        # Report
        self.logger.info('Server is initialized.')

    def start(self):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self._run)
            t.setDaemon(True)
            t.start()

    def _run(self):
        # Setup socket listener
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.IP, self.port))
        sock.listen(1)
        self.logger.info(f'Server listens on {self.IP}:{self.port}')

        # Start listening
        self.logger.info(
            f'Server starts listening, the terminal will be blocked until it stops.')
        idx = 0
        while self.running:
            # Accept new connection
            connection, client_addr = sock.accept()

            # Start new thread to handle the connection
            t = threading.Thread(target=self._handle_connection, args=(
                connection, client_addr, idx))
            t.start()
            idx = (idx + 1) % 65536

        self.logger.info(f'Server stops.')

    def _handle_connection(self, connection, addr, idx):
        # Handle [connection] on [addr]
        name = f'Handler-{idx}'
        self.logger.info(
            f'Server is connected by {connection} on {addr}, handler is {name}')

        try:
            # Fetch request
            request = connection.recv(65536).decode()
            length = len(request)
            self.logger.info(f'{name} receives {length} bytes')

            # Parse request
            content = self.resp(request)

            # Send content
            self._safe_send(content, connection, name)

        except Exception as e:
            self.logger.error(f'Runtime error on {name}: {e}')

        finally:
            connection.close()
            self.logger.info(f'{name} closed')

    def _safe_send(self, content, connection, name=None):
        # Send [content] use [connection]
        content = encode(content)
        length = len(content)
        connection.sendall(content)
        self.logger.info(f'{name} sent {length} bytes')
