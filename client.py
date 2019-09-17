import socket


class Client:
    def __init__(self):
        try:
            self.sock = socket.create_connection(('127.0.0.1', 10001))
        except ConnectionRefusedError:
            print("Server doesn't work")

    def send(self):
        try:
            with self.sock as sock:
                try:
                    while True:
                        try:
                            print('Доступные команды: "hour", "minutes", "seconds", "stop".')
                            comm = input('Введите команду: ').lower()
                            sock.sendall(comm.encode('utf-8'))
                            data = sock.recv(1024)
                            dat = data.decode('utf-8')
                            if not data:
                                break
                            if dat == 'Connection has been closed':
                                print(dat)
                                break
                            if dat == 'Connection has been closed by timeout':
                                print(dat)
                                break
                            print(dat)
                        except ConnectionAbortedError:
                            print("Connection has been aborted")
                            break
                except socket.error as err:
                    print('Error')
        except AttributeError:
            pass


Client().send()
