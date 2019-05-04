import socket
import threading
import json


class Node(object):
    def __init__(self, ip, port,cs_addr = None, cs=False):
        self.addr = (ip,port)
        self.request_number= {}
        self.ID = None
        self.cs_addr = cs_addr
        self.cs = cs
        #token = {"last_req_num":{},"queue":[]}
        self.token = None
        self.net_addr = {}
        self.monitor = None
        self.want = False


    def recieve_message(self,data,addr):
        if data["head"] == 'request_token':
            return self.receive_request(data["request_number"],addr)
        elif data["head"] == 'send_token':
            return self.receive_token(data["token"])
        elif data["head"] == 'initialize':
            return self.initialize(data["cs_addr"],addr)
        elif data["head"] == 'update':
            return self.update(data)

    def update(self,data):
        self.net_addr = data["net_info"]
        self.ID = self.net_addr[self.addr]
        for ID in self.net_addr.values():
            self.request_number[ID] = self.request_number.get(ID,0)

    def initialize(self,data,addr):
        self.cs_addr = data
        self.monitor = tuple(addr)

    def want_token(self):
        self.want = True
        if not self.token:
            return self.send_reqeust_to_everyone()
        else:
            return self.enterCS()

    def send_reqeust_to_everyone(self):
        # will establish a connection to send request
        self.request_number[self.ID] +=1
        msg = {"head": "request_token","request_number":self.request_number[self.ID]}
        to_addr = list(self.net_addr.keys())
        to_addr.remove(self.addr)
        return msg, to_addr


    # listen to the request node, will be a thread on port 60000
    def receive_request(self,request_number,from_addr):
        # will establish a connection to receive request
        print(self.addr, 'request from:', from_addr)
        ID = self.net_addr[from_addr]
        self.request_number[ID] = max(self.request_number[ID],request_number)

        if self.token:
            if not self.cs:
                if self.token["last_req_num"][ID] + 1 == self.request_number[ID]:
                    return self.send_token(self, from_addr)

    # will be a thread sending info on port 50000
    def send_token(self,addr):
        # will establish a connection to send token
        msg = {"head": "send_token","token":self.token}

        self.token = None
        return msg, addr



    def receive_token(self, token):
        self.token = token
        if self.want:
            print("enter CS")
            return self.enterCS()
        return None,None

    def enterCS(self):
        msg = {'head': "enter"}
        self.cs = True
        print("entering CS")
        return msg, self.cs_addr

    def exitCS(self):
        self.cs = False
        print("exit CS")
        self.token["last_req_num"][self.ID] = self.request_number[self.ID]
        for ID in self.request_number.keys():
            if self.request_number[ID] == self.token["last_req_num"][self.ID] + 1:
                self.token["queue"].append(ID)
        if self.token["queue"]:
            next_one = self.token["queue"].pop(0)
            for key in self.net_addr.keys():
                if self.net_addr[key] == next_one:
                    return self.send_token(key)
        return None,None


    def get_status(self):
        return {"have_token":self.token, "RN":self.request_number}

    def __repr__(self):
        return str(self.addr)