import time


class Node(object):
    def __init__(self, ip, port,parent_addr=None,cs_addr = None, cs=False, token=False):
        self.addr = (ip,port)
        self.parent = parent_addr
        self.cs_addr = cs_addr
        self.cs = cs
        self.token = token
        self.queue = []
        self.monitor = None


    def recieve_message(self,data,addr):
        if data["head"] == 'request_token':
            return self.receive_request(addr)
        elif data["head"] == 'send_token':
            return self.receive_token(addr)
        elif data["head"] == 'initialize':
            return self.initialize(data["content"],addr)

    def initialize(self,data,addr):
        self.parent = tuple(data["parent"])
        self.cs_addr = tuple(data["cs_addr"])
        self.monitor = tuple(addr)
        if data["token"]:
            self.token = True
        msg = {"head": "info", "node": self.addr, "parent": self.parent,"token": self.token}
        return msg, self.monitor

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
            return None,None
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

    def receive_token(self, holder):
        # will establish a connection to send request
        request_addr = self.queue.pop(0)
        self.token = True
        if request_addr == self.addr:
            self.parent = self.addr
            print("enter CS")
            return self.enterCS()
        else:
            print("pass token")
            self.parent = request_addr
            self.token = False
            return self.send_token(self.parent)


    def enterCS(self):
        msg = {'head': "enter"}
        self.cs = True
        print("entering CS")
        return msg, self.cs_addr

    def exitCS(self):
        self.cs = False
        print("exit CS")
        if len(self.queue) != 0:
            first_node = self.queue.pop(0)
            self.send_token(first_node)
            self.parent = first_node
            return self.send_token(self.parent)
        return None,None

    def get_queue(self):
        return [i for i in self.queue]

    def want_token(self):
        self.queue.append(self.addr)
        return self.send_reqeust_to_parent()

    def get_holder(self):
        return self.parent

    def get_status(self):
        return {"have_token":self.token, "parent":self.parent}

    def __repr__(self):
        return str(self.addr)