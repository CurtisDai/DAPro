import socket
import threading
import json
import Raymond.raymondNode
import time

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
port = int(input('your port:'))
monitor_addr = input('logger ip address:')
monitor_port = int(input('logger port:'))
monitor = (monitor_addr,monitor_port)


while True:
    algorithm = str(input('what kind of algorithm you wanna show?:'))
    if algorithm == 'raymond':
        node = Raymond.raymondNode.Node(myaddr, port)
        break
    else:
        print('no this algorithm')

# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

# receiving
class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('start listening\r\n')
        while True:
            msg, addr = s.recvfrom(2048)  # receive
            try:
                data = json.loads(msg)
                output,to_addr = node.recieve_message(data,addr)
                if to_addr:
                    output = json.dumps(output)
                    s.sendto(output.encode(), to_addr)
                if output:
                    output = json.dumps(output)
                    s.sendto(output.encode(), monitor)
            except Exception as e:
                s.sendto(str(e).encode(), addr)
                pass


# send
class send(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        msg = {"head": "login", "algorithm": algorithm}
        data = json.dumps(msg)
        s.sendto(data.encode(), monitor)  # send
        while True:
            print("Do you wanna go to critical section? (y/n)")
            try:
                letter = str(input())
                if letter.lower == "y":
                    msg,to_addr = node.want_token()
                    data = json.dumps(msg)
                    s.sendto(data.encode(), to_addr)  # send
                    s.sendto(data.encode(), monitor)
                else:
                    print("sleep for a while")
                    time.sleep(2)
            except Exception as e:
                print(e)
                pass


# start threads
thread1 = listen()
thread2 = send()
thread1.start()
thread2.start()


