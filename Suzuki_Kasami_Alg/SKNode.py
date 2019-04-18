import socket
import threading
import json
import sys
from Suzuki_Kasami_Alg.NodeProg import NodeProg

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('your port:'))

# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

serverip = input('aim address:')
serverport = int(input('aim port:'))
serveraddr = (serverip, serverport)

SuzukiNode = NodeProg(myaddr + port, myaddr, port, serverip, serverport)

cs_addr = None

# report all the information before make a move
def report(act,result,id=''):
    msg = None
    if act == 'token':
        msg = {'head':'report','type':'token','content':result}
    if act == 'request':
        msg = {'head': 'report','type':'request', 'content': result}
    if act == 'pass':
        msg = {'head': 'report','type':'pass', 'content': id}
    if act == 'enter':
        msg = {'head': 'report','type':'enter', 'content': result}
    if act == 'leave':
        msg = {'head': 'report','type':'leave', 'content': result}

    # s.sendto(json.dumps(msg).encode(),serveraddr)
    return msg

# put the cs_addr outside the algorithm
def receive_message(data,addr):
    global SuzukiNode
    global cs_addr

    if data['head'] == 'Success':
        SuzukiNode.start()
        nodeList = data['content']
        SuzukiNode.updateNodesInfo(nodeList)
        if data['ownToken'] == True:
            SuzukiNode.initTokenUponServer()
            print("[Login] Successfully")
        # TODO] server message haven't include cs address content
        cs_addr = data['cs_addr']

        return report('token',data['ownToken'])

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
            print("You have got the money: " + m)
        elif data['head'] == 'decline':
            print("Fail to receive money")

        feedback = SuzukiNode.csLeave()
        if feedback == False:
            print('No one need the token,Let me hold')
            return report('leave',True)
        elif feedback == None:
            print("I need a token")
        else:
            feed, id = feedback
            print("Token have been passed")
            return report('pass',True,id)
    else:
        pass

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

            data = json.load(msg.decode())

            # Client handling all the receiving messages
            output = receive_message(data, addr)
            output = json.dumps(output)
            s.sendto(output,serveraddr)

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
                            s.sendto(json.dumps(report('token',True)), serveraddr)
                            s.sendto(data.encode(), shaddr)  # send
                        else:
                            s.sendto(json.dumps(report('request', True)), serveraddr)
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

