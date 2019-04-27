import json
import socket
import random
host = socket.gethostname()
myaddr = socket.gethostbyname(host)
port = int(input('Set your local port:'))

print("*" * 80)
print("Monitior Information:")
print('IP address:', myaddr)
print("port: ", port)
print("*" * 80)

BUFSIZE = 2048
client = []
storehouse = None
ip_port = (myaddr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)
print("start listening")

while True:
    try:
        newNode = False
        data, client_addr = server.recvfrom(BUFSIZE)
        msg = json.loads(data)
        print('server received ', msg)

        if msg["head"] == 'login':
            if msg["algorithm"] == "raymond":
                if client:
                    i = random.randint(0,len(client)-1)
                    parent = client[i]
                else:
                    parent = client_addr
                data = {"head":'initialize', "content": {"parent":parent,"cs_addr":storehouse}}
                data = json.dumps(reply)

                client.append(client_addr)


            data = json.dumps(reply)
            server.sendto(data.encode(), client_addr)

        elif msg["head"] == 'storehouse' and msg["password"] == "storehouse":
            storehouse = client_addr

        else:
            msg = "invalid operation"
            data = json.dumps(msg)
            server.sendto(data.encode(), client_addr)

        # broadcast
        if newNode:
            msg = {"head": "update", "content": client_addr}
            data = json.dumps(msg)
            #server.sendto(data.encode(), client_addr)


    except Exception as e:
        pass

server.close()