import socket
import time
from multiprocessing import Process
from threading import Thread


class Server(Process):
    def __init__(self, port, n=3):
        super().__init__()
        self.port = port
        self.n = n

    def processes(self):
        for i in range(self.n):
            Process(target=self.connect(), args=())

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', self.port))
            sock.listen(socket.SOMAXCONN)
            while True:
                conn, addr = sock.accept()
                conn.settimeout(15)
                Thread(target=self.worker(conn))

    def worker(self, conn):
        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    comm = data.decode('utf-8')
                    t = time.ctime(time.time())
                    if comm == 'hour':
                        conn.sendall(t[-13:t.find(':')].encode('utf-8'))
                    elif comm == 'minutes':
                        conn.sendall(t[t.find(':') + 1:t.rfind(':')].encode('utf-8'))
                    elif comm == 'seconds':
                        conn.sendall(t[t.rfind(':') + 1:t.rfind(' ')].encode('utf-8'))
                    elif comm == 'stop':
                        conn.sendall('Connection has been closed'.encode('utf-8'))
                        break
                    else:
                        conn.sendall('ERROR'.encode('utf-8'))
                except socket.timeout:
                    conn.sendall('Connection has been closed by timeout'.encode('utf-8'))
                    break
                except socket.error as err:
                    print('Error', err)
                    break


if __name__ == '__main__':
    Server(10001).processes()
