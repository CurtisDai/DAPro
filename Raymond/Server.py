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
        self.gui = UI.UI(self.window)
        self.starting()
        self.gui.add_node("CS")

    def start_listen(self):
        global operation_count
        global num

        while True:
            data, client_addr = server.recvfrom(BUFSIZE)
            msg = json.loads(data)
            print(msg)
            info_buf.append(msg)
            if msg["head"] == 'login':
                token = False
                client_ID[tuple(client_addr)] = str(num)
                self.gui.add_node(str(num))

                num += 1

                if algorithm == "raymond":
                    if client:
                        i = random.randint(0, len(client) - 1)
                        parent = client[i]
                    else:
                        parent = client_addr
                        token = True

                    data = {"head": 'initialize', "algorithm": algorithm,
                            "content": {"parent": parent, "cs_addr": storehouse, "token": token}}
                    data = json.dumps(data)
                    if client_addr not in client:
                        client.append(client_addr)

                    server.sendto(data.encode(), client_addr)

            prefix = '[' + str(operation_count) + ']:'

            if msg["head"] == "log":
                first_node = client_ID[tuple(msg["from"])]
                second_node = client_ID[tuple(msg["to"])]
                if (first_node, second_node) not in self.gui.edge_id:
                    self.gui.edge_id[first_node, second_node] = self.gui.add_edge(first_node, second_node,prefix + str(msg["msg"]))
                else:
                    self.gui.update_edge(first_node, second_node, prefix + str(msg["msg"]))

            elif msg["head"] == "info":
                print(msg["node"])
                node = client_ID[tuple(msg["node"])]
                self.gui.update_node(node, prefix + node + str(msg['parent']) + str(msg['token']))

            operation_count += 1

            time.sleep(5)
        server.close()


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
    cs_addr = "10.12.175.94"
    cs_port = 7000
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
    client = []
    storehouse = cs_location

    client_ID = {}

    num = 0
    client_ID[cs_location] = "CS"

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


