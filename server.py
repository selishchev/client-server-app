import socket
import time
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor


class Server(Process):
    def __init__(self, port):
        super().__init__()
        self.port = port

    #@staticmethod
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', self.port))
            sock.listen(socket.SOMAXCONN)
            while True:
                conn, addr = sock.accept()
                conn.settimeout(15)
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
                                conn.sendall(t[t.find(':')+1:t.rfind(':')].encode('utf-8'))
                            elif comm == 'seconds':
                                conn.sendall(t[t.rfind(':')+1:t.rfind(' ')].encode('utf-8'))
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

    #@staticmethod
    def work(self):
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.submit(Server(self.port).connect())


if __name__ == '__main__':
    p1 = Process(target=Server(10000).work, args=())
    p2 = Process(target=Server(10001).work, args=())
    p3 = Process(target=Server(10002).work, args=())
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
