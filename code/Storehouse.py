import socket
import threading
import sys
import json

MONEY = 100

# receiving
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global MONEY
        print('start listening\r\n')
        while True:
            msg,addr = s.recvfrom(2048)
            try:
                msg = json.loads(msg)
                if msg["head"] == "givememoney":
                    if MONEY >=100:
                        data = {"head": "money", "content": 100}
                        MONEY -= 100
                    else:
                        data = {"head": "decline", "content": "nomoney"}

                    s.sendto(json.dumps(data).encode(), addr)
                print('\nreceive from' + str(addr) + ':\n\t' + msg.decode() + '\n:')
            except Exception as e:
                s.sendto(str(e).encode(), addr)
                pass




# start threads



if __name__ == '__main__':
    if len(sys.argv) ==3:
        try:
            serv_ip = sys.argv[1]
            serv_port = int(sys.argv[2])
            server_ip_port = (serv_ip, serv_port)

        except Exception as e:
            sys.stderr.write("Need server's IP address and port\n")
            sys.exit()
    else:
        sys.stderr.write("Need server's IP address and port\n")
        sys.exit()

    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)
    print('logger ip address:', myaddr)
    port = int(input('your port:'))

    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    data = {"head": "storehouse", "password": "storehouse"}
    s.sendto(json.dumps(data).encode(), server_ip_port)

    thread = server()
    thread.start()
