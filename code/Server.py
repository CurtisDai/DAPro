import json
import socket
import random
import tkinter as tk
from Raymond import UI

window = tk.Tk()
node_name = ['0', '1', '2', '3', '4', '5']
ui = UI.UI(window, node_name)


host = socket.gethostname()
myaddr = socket.gethostbyname(host)
port = int(input('Set your local port:'))
algorithm = None

while True:
    enter = str(input('what kind of algorithm you wanna show?(RM/SK)\n'))
    if enter == 'RM':
        algorithm = "raymond"
        break
    elif enter == 'SK':
        algorithm = "suzuki"
        break
    else:
        print('bad choice')

cs_addr = input("cs ip address:")
cs_port = int(input('cs port:'))
cs_location = (cs_addr, cs_port)

# socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((host, port))
data = {"head": "storehouse", "password": "storehouse"}

print("*" * 80)
print("Network Information: ")
print('Monitor IP address: ', myaddr)
print("Monotor port: ", port)
print("CS IP address: ",cs_addr)
print("CS port: ",cs_port)
print("*" * 80)


BUFSIZE = 2048
client = []
storehouse = None
ip_port = (myaddr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)




print("start listening")


operation_count = 0

# keyboard_input = input('options:\n0.updateNode\n1.createEdge\n2.updateEdge\n')
# operation_count = 0
# while keyboard_input != 'q':
#     prefix = '[' + str(operation_count) + ']:'
#
#     if keyboard_input == '0':
#         keyboard_input = input('Enter the node\'s name needs update\n')
#         ui.update_node(keyboard_input, prefix + keyboard_input + ' has been updated.')
#
#     elif keyboard_input == '1':
#         first_node = input('Enter first node\'s name of edge to create\n')
#         second_node = input('Enter second node\'s name of edge to create\n')
#         if first_node != second_node and (first_node, second_node) not in ui.edge_id:
#             ui.edge_id[first_node, second_node] = ui.add_edge(first_node, second_node, prefix + 'new edge created')
#         else:
#             print('Plz enter valid node\'s name')
#     elif keyboard_input == '2':
#         first_node = input('Enter first node\'s name of edge to update\n')
#         second_node = input('Enter second node\'s name of edge to update\n')
#         if (first_node, second_node) in ui.edge_id:
#             ui.update_edge(first_node, second_node, prefix + ':existed edge updated')
#         else:
#             print('Plz create edge first.')
#
#     operation_count += 1
#     keyboard_input = input('options:\n0.updateNode\n1.createEdge\n2.updateEdge\n')
#
#

while True:
    data, client_addr = server.recvfrom(BUFSIZE)
    msg = json.loads(data)

    print('server received: ', msg)
    if msg["head"] == 'login':
        token = False
        if algorithm == "raymond":
            if client:
                i = random.randint(0,len(client)-1)
                parent = client[i]
            else:
                parent = client_addr
                token = True

            data = {"head":'initialize', "algorithm":algorithm,
                    "content": {"parent": parent, "cs_addr": storehouse, "token":token}}
            data = json.dumps(data)
            client.append(client_addr)

            prefix = '[' + str(operation_count) + ']:'
            ui.update_node(len(client)-1, prefix + str(len(client)-1) + ' has been initialized.')


            server.sendto(data.encode(), client_addr)

    operation_count += 1

window.destroy()
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


