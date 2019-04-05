
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
        data, client_addr = server.recvfrom(BUFSIZE)
        if client_addr not in client:
            client.append(client_addr)
        print('server收到的数据', data.decode())
        if data.decode() == 'login':
            server.sendto(("success").encode(), client_addr)
            server.sendto(str(client).encode(), client_addr)
        else:
            server.sendto(("invalid operation").encode(), client_addr)
    except Exception as e:
        pass

server.close()