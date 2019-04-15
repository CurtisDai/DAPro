import socket
import threading
import json
import sys
sys.path.append('.')
sys.path.append('.\Suzuki_Kasami_Alg')
from Suzuki_Kasami_Alg.NodeProg import NodeProg

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print(myaddr)
print('logger ip address:', myaddr)
port = int(input('your port:'))
SuzukiNode = None

# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

serverip = input('aim address:')
serverport = int(input('aim port:'))
serveraddr = (serverip, serverport)

# report all the information before make a move
def report(act,id=''):
    msg = None
    if act == 'token':
        msg = {'head':'report','type':'token','content':True}
    if act == 'request':
        msg = {'head': 'report','type':'request', 'content': True}
    if act == 'pass':
        msg = {'head': 'report','type':'pass', 'content': id}
    if act == 'enter':
        msg = {'head': 'report','type':'enter', 'content': True}
    if act == 'leave':
        msg = {'head': 'report','type':'leave', 'content': True}

    s.sendto(json.dumps(msg).encode(),serveraddr)


# receiving
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._listening = True

    def run(self):
        print('start listening\r\n')
        while self._listening:
            msg, addr = s.recvfrom(2048)  # receive
            try:
                print('\nreceive from' + str(addr) + ':\n\t' + msg.decode() + '\n:')
            except Exception as e:
                s.sendto(str(e).encode(), addr)

            # Client handling all the receiving messages
            global SuzukiNode
            data = json.load(msg.decode())
            if data['head'] == 'Success':
                SuzukiNode = NodeProg(myaddr+port,addr,port,serverip,serverport)
                SuzukiNode.start()
                nodeList = data['content']
                SuzukiNode.updateNodesInfo(nodeList)
                if data['ownToken'] == True:
                    SuzukiNode.initTokenUponServer()
                    print("[Login] Successfully")
            elif data['head'] == 'update':
                if SuzukiNode is not None:
                    node = data['content']
                    SuzukiNode.updateNodesInfo([node])
                    print("[Update] My list upon new node")
                else:
                    print("[You have not login]")
            elif data['head'] == 'money' or data['head'] == 'decline':
                if data['head'] == 'money':
                    m = data['content']
                    print("You have got the money: "+ m)
                elif data['head'] == 'decline':
                    print("Fail to receive money")

                feedback = SuzukiNode.csLeave()
                if feedback == False:
                    print('No one need the token,Let me hold')
                elif feedback == None:
                    print("I need a token")
                else:
                    print("Token have been passed")
            else:
                pass




    def close(self):
        self._listening = False
        s.close()


# send
class client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._listening = True

    def run(self):
        while self._listening:
            print("what you wanna do now?(reply the number)")
            print("1. login")
            print("2. go to storehouse")

            global SuzukiNode

            try:
                num = int(input())
                if num == 1:
                    msg = {"head": "login", "password": "edon"}
                    data = json.dumps(msg)
                    s.sendto(data.encode(), serveraddr)  # send
                elif num == 3:
                    ship = input('aim address:')
                    shport = int(input('aim port:'))
                    shaddr = (ship, shport)
                    msg = {"head": "givemoney"}
                    data = json.dumps(msg)

                    # request token before enter cs
                    if SuzukiNode is not None:
                        assert isinstance(SuzukiNode,NodeProg)
                        if SuzukiNode.csEnter():
                            s.sendto(data.encode(), shaddr)  # send
                    else:
                        print("You haven't login")



                else:
                    print("not offer this service now")
            except Exception as e:
                print(e)
                pass

    def close(self):
        self._listening = False

# start threads
thread1 = server()
thread2 = client()
try:
    thread1.start()
    thread2.start()
except KeyboardInterrupt:
    thread1.close()
    thread2.close()

