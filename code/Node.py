import socket
import threading
import json

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('your port:'))


# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))


# receiving
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('start listening\r\n')
        while True:
            msg, addr = s.recvfrom(2048)  # 接收
            try:
             print('\nreceive from' + str(addr) + ':\n\t' + msg.decode() + '\n:')
            except Exception as e:
                s.sendto(str(e).encode(), addr)
                pass


# send
class client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print("what you wanna do now?(reply the number)")
            print("1. login")
            print("2. send to other node")
            print("3. go to storehouse")

            try:
                num = int(input())
                if num == 1:
                    serverip = input('aim address:')
                    serverport = int(input('aim port:'))
                    serveraddr = (serverip, serverport)
                    msg = {"head": "login", "password": "edon"}
                    data = json.dumps(msg)
                    s.sendto(data.encode(), serveraddr)  # send
                elif num == 2:
                    nodeip = input('aim address:')
                    nodeport = int(input('aim port:'))
                    nodeaddr = (nodeip, nodeport)
                    msg = {"head": "node", "password": "node"}
                    data = json.dumps(msg)
                    s.sendto(data.encode(), nodeaddr )  # send
                elif num == 3:
                    ship = input('aim address:')
                    shport = int(input('aim port:'))
                    shaddr = (ship, shport)
                    msg = {"head": "givemoney"}
                    data = json.dumps(msg)
                    s.sendto(data.encode(), shaddr)  # send

                else:
                    print("not offer this service now")
            except Exception as e:
                print(e)
                pass


# start threads
thread1 = server()
thread2 = client()
thread1.start()
thread2.start()


