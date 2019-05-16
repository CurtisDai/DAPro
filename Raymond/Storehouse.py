import socket
import threading
import json
import time
import sys

class CriticalSection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            msg,addr = s.recvfrom(2048)
            try:
                msg = json.loads(msg)
                if msg["head"] == "enter":
                    print(addr," is using the critical section")
                    time.sleep(2)
            except Exception as e:
                print(e)
                pass


# start threads
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(input('Set your local port:'))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)
    s.bind((myaddr, port))
    print("*" * 80)
    print("address: ", myaddr)
    print("port: ", port)
    print("*" * 80)
    print('start listening\r\n')

    thread = CriticalSection()
    thread.start()
