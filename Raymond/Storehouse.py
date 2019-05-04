import socket
import threading
import json
import time
MONEY = 100

# receiving
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global MONEY
        print('start listening\r\n')
        host = socket.gethostname()
        myaddr = socket.gethostbyname(host)
        print("my address: ",myaddr)
        while True:
            msg,addr = s.recvfrom(2048)
            try:
                msg = json.loads(msg)
                if msg["head"] == "enter":
                    print(addr," is using the critical section")
                    time.sleep(2)
            except Exception as e:
                s.sendto(str(e).encode(), addr)
                pass


# start threads
if __name__ == '__main__':
    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)
    port = int(input('your port:'))
    # socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))

    thread = server()
    thread.start()
