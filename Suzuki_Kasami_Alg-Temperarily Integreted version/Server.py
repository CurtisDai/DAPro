import json
import socket

host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('local port:'))

BUFSIZE = 1024
client = []
storehouse = ()
ip_port = (myaddr, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)
print("start listening")

def handleReport(msg):
    act = msg['type']
    if act == 'token':
        pass
    if act == 'request':
        pass
    if act == 'pass':
        content = msg['content']
    if act == 'enter':
        pass
    if act == 'leave':
        pass


while True:
    try:
        newNode = False
        data, client_addr = server.recvfrom(BUFSIZE)
        msg = json.loads(data.decode())
        print('server received ', msg)

        if msg["head"] == 'login' and msg["password"] == "edon":
            if client_addr not in client:
                newNode = True
                client.append(client_addr)

            # The ownToken indicate the first node to initial the token
            if len(client) == 1:
                reply = {"head": "Success", "content": client,"ownToken":True}
            else:
                reply = {"head": "Success", "content": client,"ownToken":False}
            data = json.dumps(reply)
            server.sendto(data.encode(), client_addr)

        elif msg["head"] == 'storehouse' and msg["password"] == "storehouse":
            storehouse = client_addr
        elif msg['head'] == 'report':
            handleReport(msg)
        else:
            msg = "invalid operation"
            data = json.dumps(msg)
            server.sendto(data.encode(), client_addr)

        # broadcast
        if newNode:
            for cAddr in client:
                msg = {"head": "update", "content": client_addr}
                data = json.dumps(msg)
                server.sendto(data.encode(), cAddr)

    except KeyboardInterrupt:
        break

# server.close()
