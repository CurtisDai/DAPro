import json
import socket
import random
import threading
import tkinter as tk
import UI
import time

class ThreadClient():
    def __init__(self, window):
        self.window = window

        self.starting()
        self.gui = UI.UI(self.window,algorithm,False)
        self.gui.add_node("CS")
        self.client_ID = {}
        self.client_ID[cs_location] = "CS"
        if algorithm == "suzuki":
            self.tokenholder = None

    def start_listen(self):
        global operation_count
        global num

        while True:
            data, client_addr = server.recvfrom(BUFSIZE)
            client_addr = tuple(client_addr)
            msg = json.loads(data.decode())
            print(msg)
            info_buf.append(msg)
            if msg["head"] == 'login':
                token = False # ?????
                num += 1
                self.client_ID[client_addr] = str(num)
                self.gui.add_node(str(num))

                if algorithm == "raymond":
                    if client:
                        i = random.randint(0, len(client) - 1)
                        parent = client[i]
                    else:
                        parent = client_addr
                        token = True

                    data = {"head": 'initialize', "algorithm": algorithm,
                            "content": {"parent": parent,"cs_addr": storehouse, "token": token}}
                    data = json.dumps(data)
                    if client_addr not in client:
                        client.append(client_addr)

                    server.sendto(data.encode(), client_addr)
                else:
                    ownToken = False
                    if not self.tokenholder:
                        self.tokenholder = client_addr
                        ownToken = True
                        self.gui.draw_token(self.client_ID[self.tokenholder])

                    allnodes = []
                    # the value is id, key is [ip,port]
                    for key,value in self.client_ID.items():
                        if value == 'CS':
                            allnodes.append((value,key))
                        else:
                            ip,port = key
                            allnodes.append((value,[ip,port+1]))

                    data = {"head": 'initialize', "algorithm": algorithm,
                            "content": {"allnodes": allnodes, "ownToken":ownToken,"id":str(num)}}

                    # data = {"head": 'update',"net_info": self.client_ID, "token": token}
                    data = json.dumps(data)
                    server.sendto(data.encode(), client_addr)
                    #client.append(client_addr)
                    ip,port = client_addr
                    data = {"head": 'update', "content": [self.client_ID[client_addr],[ip,port+1]]}
                    data = json.dumps(data)
                    for addr,id in self.client_ID.items():
                        if addr != client_addr and id != 'CS':
                            server.sendto(data.encode(),addr)

            prefix = '[' + str(operation_count) + ']:'

            if msg["head"] == "log":
                if algorithm == 'raymond':
                    first_node = self.client_ID[tuple(msg["from"])]
                    second_node = self.client_ID[tuple(msg["to"])]
                    if (first_node, second_node) not in self.gui.edge_id:
                        self.gui.add_edge(first_node, second_node,prefix + str(msg["msg"]))
                    else:
                        self.gui.update_edge(first_node, second_node, prefix + str(msg["msg"]))
                    self.gui.update_node(first_node, prefix + str(msg['status']))
                else:
                    msgType = msg['type']
                    id = msg['content']
                    if msgType == 'request':
                        operation_count += 1
                        self.gui.delete_all_edge()
                        for targetId in self.client_ID.values():
                            if (id,targetId) not in self.gui.edge_id:
                                if targetId != id and targetId != 'CS':
                                    self.gui.add_edge(id,targetId,prefix + msgType) # What the meaning of msg
                            else:
                                self.gui.update_edge(id,targetId,prefix+msgType)
                    if msgType == 'recvtoken':
                        operation_count += 1
                        fromId = msg['result']
                        if (fromId, id) not in self.gui.edge_id:
                            self.gui.add_edge(fromId, id, prefix + msgType)  # What the meaning of msg
                        else:
                            self.gui.update_edge(fromId, id, prefix + msgType)
                        self.gui.draw_token(id)
                    if msgType == 'enter':
                        operation_count += 1
                        toId = 'CS'
                        if (id, toId) not in self.gui.edge_id:
                            self.gui.add_edge(id, toId, prefix + msgType)  # What the meaning of msg
                        else:
                            self.gui.update_edge(id, toId, prefix + msgType)

                    if msgType == 'leave':
                        operation_count += 1
                        fromId = 'CS'
                        if (fromId, id) not in self.gui.edge_id:
                            self.gui.add_edge(fromId, id, prefix + msgType)  # What the meaning of msg
                        else:
                            self.gui.update_edge(fromId, id, prefix + msgType)

            elif msg["head"] == "info":
                if algorithm == 'raymond':
                    print(msg["node"])
                    node = self.client_ID[tuple(msg["node"])]
                    self.gui.update_node(node, prefix + node + str(msg['parent']) + str(msg['token']))
                else:
                    pass
                    #print(msg)

            #time.sleep(5)

    def starting(self):
        self.thread = threading.Thread(target=self.start_listen)
        self.thread.start()


if __name__ == '__main__':
    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)

    # port = int(input('Set your local port:'))
    #
    # if not port:
    #     port = 8086
    # address = (myaddr, port)
    # algorithm = None
    # while True:
    #     enter = str(input('what kind of algorithm you wanna show?(RM/SK)\n'))
    #     if enter == 'RM':
    #         algorithm = "raymond"
    #         break
    #     elif enter == 'SK':
    #         algorithm = "suzuki"
    #         break
    #     else:
    #         print('bad choice')
    #
    # cs_addr = input("cs ip address:")
    # cs_port = int(input('cs port:'))
    # cs_location = (cs_addr, cs_port)

    port = 6000
    cs_addr = '169.254.213.193'
    cs_port = 7000
    cs_location = (cs_addr, cs_port)
    address = (myaddr, port)
    #algorithm = "raymond"
    algorithm = 'suzuki'
    print("*" * 80)
    print("Network Information: ")
    print('Monitor IP address: ', myaddr)
    print("Monotor port: ", port)
    print("CS IP address: ", cs_addr)
    print("CS port: ", cs_port)
    print("*" * 80)

    BUFSIZE = 2048
    client = []
    storehouse = cs_location



    num = 0


    print("start listening")

    info_buf = []
    node_dict = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建TCP socket
    server.bind(address)  # 绑定地址
    keepalive = False
    operation_count = 0

    window = tk.Tk()
    tool = ThreadClient(window)
    window.mainloop()
    tool.starting()








        # elif algorithm == "suzuki":
        #     if client:
        #         update = {"head": "update", "content": client_addr}
        #         update = json.dumps(update)
        #         for addr in client:
        #             server.sendto(update.encode(),addr)
        #
        #         client.append(client_addr)
        #         data = {"head": 'initialize', "algorithm": algorithm, "content": {"nodelist": client, "cs_addr": storehouse}}
        #         data = json.dumps(data)
        #         server.sendto(data.encode(), client_addr)
        #     else:
        #         token = True


