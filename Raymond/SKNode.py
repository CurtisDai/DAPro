import socket
import threading
import json


class Node(object):
    def __init__(self, ip, port,nodelist=None,cs_addr = None, cs=False, token=False):
        self.addr = (ip,port)
        self.nodelist = nodelist
        self.cs_addr = cs_addr
        self.cs = cs
        self.token = token
        self.queue = []

    # put the cs_addr outside the algorithm
    def receive_message(self,data, addr):

        if data['head'] == 'initialize':
            nodeList = data['content']
            SuzukiNode.updateNodesInfo(nodeList)
            if data['ownToken'] == True:
                SuzukiNode.initTokenUponServer()
                print("[Login] Successfully")
            # TODO] server message haven't include cs address content
            cs_addr = data['cs_addr']

            return report('token', data['ownToken']), None

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
                return report('leave', True), None
            elif feedback == None:
                print("I need a token")
            else:
                feed, id = feedback
                print("Token have been passed")
                return report('pass', True, id), None
        else:
            pass

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


#################

    def recieve_message(self,data,addr):
        if data["head"] == 'request_token':
            return self.receive_request(addr)
        elif data["head"] == 'send_token':
            return self.receive_token(addr)
        elif data["head"] == 'initialize':
            return self.initialize(data["content"])

    def initialize(self,data):
        self.parent = data["parent"]
        self.cs_addr = data["cs_addr"]
        return "Success initialized"

    # listen to the request node, will be a thread on port 60000
    def receive_request(self,child_addr):
        # will establish a connection to receive request
        print(self.addr, 'request from:', child_addr)
        self.queue.append(child_addr)
        if self.token:
            if not self.cs:
                first_node = self.queue.pop(0)
                self.parent = first_node
                self.token = False
                return self.send_token(self.parent)
        elif len(self.queue) == 1:
                return self.send_reqeust_to_parent()

    # will be a thread sending info on port 50000
    def send_token(self, parent):
        # will establish a connection to send token
        msg = {"head": "send_token"}
        to_addr = parent
        return msg, to_addr

    # listen to the receiver node, will be a thread on port 60000
    def send_reqeust_to_parent(self):
        # will establish a connection to send request
        msg = {"head": "request_token"}
        to_addr = self.parent
        return msg, to_addr

    # will be a thread listening on port 50000
    def receive_token(self, holder):
        # will establish a connection to send request
        request_addr = self.queue.pop(0)
        self.token = True
        if request_addr == self.addr:
            self.parent = self.addr
            return self.enterCS()
        else:
            self.parent = request_addr
            self.token = False
            self.send_token(self.parent)
            if (len(self.queue) != 0):
                self.send_reqeust_to_parent()

    def enterCS(self):
        msg = {'head': "enter"}
        self.cs = True
        time.sleep(2)
        return msg, self.cs_addr

    def exitCS(self):
        self.CS = False
        if len(self.queue) != 0:
            first_node = self.queue.pop(0)
            self.send_token(first_node)
            self.parent = first_node
            msg = {'head': 'send_'}
            return self.send_token(self.parent)

    def get_queue(self):
        return [i for i in self.queue]

    def want_token(self):
        self.queue.append(self)
        return self.send_reqeust_to_parent()

    def get_holder(self):
        return self.parent

    def __repr__(self):
        return str(self.addr)