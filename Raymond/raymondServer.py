import json
import socket
import random
import threading
import tkinter as tk
import UI
import time
import sys


class ThreadClient():
    def __init__(self, window):
        self.window = window
        self.gui = UI.UI(self.window, "Raymond Mutual Exclusion Stimulator", True)
        self.gui.add_node("cs")
        self.client = []
        self.cs = cs_location
        self.starting()

    # listen thread to collect information transferring between nodes
    def start_listen(self):
        global operation_count
        global num

        while True:
            # read data from buf
            data, client_addr = server.recvfrom(BUFSIZE)
            client_addr = tuple(client_addr)
            msg = json.loads(data)
            # print(msg)
            if msg["head"] == 'login':
                token = False
                self.gui.add_node(str(num))  # add new node to the UI
                num += 1
                if self.client:  # allocate a parent to the new node randomly
                    i = random.randint(0, len(self.client) - 1)
                    parent = self.client[i]
                else:  # if the first node, set parent to itself and give it the token
                    parent = client_addr
                    token = True

                if client_addr not in self.client:
                    self.client.append(client_addr)

                # send initialisation infomation to node
                data = {"head": 'initialize', "algorithm": algorithm,
                        "content": {"parent": parent,"cs_addr": storehouse, "token": token}}
                # print(self.client.index(client_addr))
                # print(self.client.index(parent))
                data = json.dumps(data)
                server.sendto(data.encode(), client_addr)

                # add the tree relationship between the node and its parent
                self.gui.add_parent(str(self.client.index(client_addr)), str(self.client.index(parent)))

            prefix = '[' + str(operation_count) + ']:'  # use to mark the sequence of msg
            if msg["head"] == "log":

                first_node = str(self.client.index(tuple(msg["from"])))
                if tuple(msg["to"]) == self.cs:
                    second_node = "cs"
                else:
                    second_node = str(self.client.index(tuple(msg["to"])))

                if (first_node, second_node) not in self.gui.edge_id:
                    self.gui.add_edge(first_node, second_node, prefix + str(msg["msg"]))
                else:
                    self.gui.update_edge(first_node, second_node, prefix + str(msg["msg"]))

                self.gui.update_node(first_node,"token: " + str(msg['status']['have_token']))
                self.gui.add_parent(first_node, str(self.client.index(tuple(msg['status']['parent']))))

                if msg['status']['have_token']:
                        self.gui.draw_token(first_node)

                operation_count += 1

            elif msg["head"] == "info":
                # print(msg["node"])
                node = str(self.client.index(tuple(msg["node"])))
                self.gui.update_node(node, str(msg['token']))
                self.gui.add_parent(node, str(self.client.index(tuple(msg["parent"]))))

                if msg['token'] == True:
                    self.gui.draw_token(node)

            time.sleep(2)
        server.close()

    # start method
    def starting(self):

        self.thread = threading.Thread(target=self.start_listen)
        self.thread.start()


if __name__ == '__main__':
    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(input('Set your local port:'))

    if len(sys.argv) > 2:
        cs_addr = sys.argv[2]
    else:
        cs_addr = input("cs ip address:")

    if len(sys.argv) > 3:
        cs_port = int(sys.argv[3])
    else:
        cs_port = int(input('cs port:'))

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

    print("start listening")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create socket
    server.bind(address)  # bind the (IP,port)

    operation_count = 0
    num = 0  # node number which printed on GUI

    window = tk.Tk()
    tool = ThreadClient(window)
    window.mainloop()








