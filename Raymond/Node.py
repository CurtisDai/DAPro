import socket
import threading
import json
import raymondNode
import SKNode
import time

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
port = int(input('your port:'))
# monitor_addr = input('logger ip address:')
# monitor_port = int(input('logger port:'))
monitor_addr = "10.12.175.94"
monitor_port = 6000
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
        print('start listening\r\n')
        global node
        while True:
            msg, addr = s.recvfrom(2048)  # receive

            data = json.loads(msg)
            if data['head'] == 'initialize':
                if data["algorithm"] == "raymond":
                    node = raymondNode.Node(myaddr,port)
                else:
                    node = SKNode.Node(myaddr,port)
            if node:
                output,to_addr = node.recieve_message(data,addr)
                print(output,to_addr)
                if to_addr:
                    msg_sending(output,to_addr)

                if output:
                    if output["head"] == "enter":
                        time.sleep(2)
                        msg, to_addr = node.exitCS()
                        if to_addr:
                            msg_sending(msg, to_addr)

# send
class send(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        msg = {"head":"login"}
        msg = json.dumps(msg)
        s.sendto(msg.encode(), monitor)  # send
        while True:
            if node:
                print("Do you wanna go to critical section? (y/n)")
                letter = str(input())
                if letter.lower() == "y":
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


