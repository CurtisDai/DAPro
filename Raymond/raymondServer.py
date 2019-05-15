import json
import socket
import random
import threading
import tkinter as tk
import UI
import time
import sys


class ThreadClient():
    def __init__(self,window):
        self.window = window
        self.gui = UI.UI(self.window)
        self.starting()
        self.gui.add_node("cs")
        self.client = []
        self.cs = cs_location

    # listen thread to collect information transferring between nodes
    def start_listen(self):
        global operation_count
        global num

        while True:
            data, client_addr = server.recvfrom(BUFSIZE)
            client_addr = tuple(client_addr)
            msg = json.loads(data)
            print(msg)
            info_buf.append(msg)
            if msg["head"] == 'login':
                token = False
                self.gui.add_node(str(num))
                num += 1
                if algorithm == "raymond":
                    if self.client:
                        i = random.randint(0, len(self.client) - 1)
                        parent = self.client[i]
                    else:
                        parent = client_addr
                        token = True
                    if client_addr not in self.client:
                        self.client.append(client_addr)

                    data = {"head": 'initialize', "algorithm": algorithm,
                            "content": {"parent": parent,"cs_addr": storehouse, "token": token}}
                    print(self.client.index(client_addr))
                    print(self.client.index(parent))
                    self.gui.add_parent(str(self.client.index(client_addr)), str(self.client.index(parent)))
                    data = json.dumps(data)

                    server.sendto(data.encode(), client_addr)


            prefix = '[' + str(operation_count) + ']:'

            if msg["head"] == "log":

                first_node = str(self.client.index(tuple(msg["from"])))
                if tuple(msg["to"]) == self.cs:
                    second_node = "cs"
                else:
                    second_node = str(self.client.index(tuple(msg["to"])))

                if (first_node, second_node) not in self.gui.edge_id:
                    self.gui.add_edge(first_node, second_node,prefix + str(msg["msg"]))
                else:
                    self.gui.update_edge(first_node, second_node, prefix + str(msg["msg"]))
                self.gui.update_node(first_node, prefix + str(msg['status']))

                if algorithm == "raymond":
                    self.gui.add_parent(first_node, str(self.client.index(tuple(msg['status']['parent']))))

            elif msg["head"] == "info":
                print(msg["node"])
                node = str(self.client.index(tuple(msg["node"])))
                self.gui.update_node(node, prefix + str(msg['token']))
                if algorithm == "raymond":
                    self.gui.add_parent(node,str(self.client.index(tuple(msg["parent"]))))

            operation_count += 1
            time.sleep(2)
        server.close()


    # start method
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
    if sys.argv[1]:
        port = int(sys.argv[1])
    else:
        port = int(input('Set your local port:'))

    if sys.argv[2]:
        cs_addr = sys.argv[2]
    else:
        cs_addr = input("cs ip address:")

    if sys.argv[3]:
        cs_port = int(sys.argv[3])
    else:
        cs_port = int(input('cs port:'))

    #
    #
    # cs_addr = "10.12.161.119"
    # cs_port = 6666
    #
    cs_location = (cs_addr, cs_port)
    address = (myaddr, port)
    algorithm = "raymond"

    print("*" * 80)
    print("Network Information: ")
    print('Monitor IP address: ', myaddr)
    print("Monotor port: ", port)
    print("CS IP address: ", cs_addr)
    print("CS port: ", cs_port)
    print("*" * 80)

    BUFSIZE = 2048

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








