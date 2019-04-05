import socket
import threading


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
            print("1. send message")
            print("2. get all node addresses")
            print("3. edit the file")

            try:
                num = int(input())
                if num == 1:
                    cliip = input('aim address:')
                    cliport = int(input('aim port:'))
                    cliaddr = (cliip, cliport)
                    data = input(':')
                    s.sendto(data.encode(), cliaddr)  # send
                else:
                    print("not offer this service now")
            except Exception as e:
                print("invalid try")
                pass


# start threads
thread1 = server()
thread2 = client()
thread1.start()
thread2.start()

