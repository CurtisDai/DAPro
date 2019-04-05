import json
import socket

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('本地端口:'))

BUFSIZE = 1024
client = []
ip_port = (myaddr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)
print("start listening")

while True:
    try:
        newNode = False
        data, client_addr = server.recvfrom(BUFSIZE)
        msg = json.loads(data)
        print('server收到的数据', msg)

        if msg["head"] == 'login' and msg["password"] == "edon":
            if client_addr not in client:
                newNode = True
                client.append(client_addr)

            reply = {"head": "Success", "content": client}
            data = json.dumps(reply)
            server.sendto(data.encode(), client_addr)

        elif msg["head"] == 'storehouse' and msg["password"] == "storehouse":

            if client_addr not in client:
                newNode = True
                client.append(client_addr)

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
