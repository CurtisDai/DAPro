import socket
import threading
import json
import raymondNode
import time
import sys


host = socket.gethostname()
myaddr = socket.gethostbyname(host)


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = int(input('Set your local port:'))

if len(sys.argv) > 2:
    monitor_addr = sys.argv[2]
else:
    monitor_addr = input("monitor ip address:")

if len(sys.argv) > 3:
    monitor_port = int(sys.argv[3])
else:
    monitor_port = int(input('monitor port:'))

address = (myaddr, port)


monitor = (monitor_addr,monitor_port)
# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
node = None
# receiving

def msg_sending(msg,to_addr):
    msg = json.dumps(msg)
    s.sendto(msg.encode(), to_addr)
    if to_addr != monitor:
        pack = {"head": "log", "from": (myaddr, port), "to": to_addr, "msg": msg,"status": node.get_status()}
        pack = json.dumps(pack)
        s.sendto(pack.encode(), monitor)

class listen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cost
        print('start listening\r\n')
        global node
        while True:
            msg, addr = s.recvfrom(2048)  # receive

            data = json.loads(msg)
            if data['head'] == 'initialize':
                node = raymondNode.Node(myaddr,port)

            if node:
                output,to_addr = node.recieve_message(data,addr)
                print(output,to_addr)
                if to_addr:
                    msg_sending(output,to_addr)

                if output:
                    if output["head"] == "enter":
                        cost = time.time() - cost
                        print("entertime - request time",cost)
                        cost = time.time()
                        time.sleep(2)
                        msg, to_addr = node.exitCS()
                        if to_addr:
                            msg_sending(msg, to_addr)

# send
class send(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global cost
        msg = {"head":"login"}
        msg = json.dumps(msg)
        s.sendto(msg.encode(), monitor)  # send
        while True:
            if node:
                print("Do you wanna go to critical section? (y/n)")
                letter = str(input())
                if letter.lower() == "y":
                    cost = time.time()
                    msg, to_addr = node.want_token()
                    if type(to_addr) is list:
                        for addr in to_addr:
                            msg_sending(msg, addr)
                    else:
                        msg_sending(msg, to_addr)

                else:
                    print("sleep for a while")
            time.sleep(5)




# start threads
thread1 = listen()
thread2 = send()
thread1.start()
thread2.start()


