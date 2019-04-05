import socket
import threading

# 输入
host = socket.gethostname()
myaddr = socket.gethostbyname(host)
print('logger ip address:', myaddr)
port = int(input('本地端口:'))
cliip = input('目标地址:')
cliport = int(input('目标端口:'))
cliaddr = (cliip, cliport)
print('尝试与目标地址 ' + str(cliaddr) + '连接\n')

# 创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))


# 接收
class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('开启服务端\r\n')
        while True:
            msg, addr = s.recvfrom(2048)  # 接收
            print('\n接收来自' + str(addr) + '的信息:\n\t' + msg.decode() + '\n：')


# 发送
class client(threading.Thread):
    def __init__(self, cliip, cliport):
        threading.Thread.__init__(self)
        self.cliaddr = cliaddr

    def run(self):
        while True:
            date = input('：')
            s.sendto(date.encode(), cliaddr)  # 发送


# 启动线程
thread1 = server()
thread2 = client(cliip,cliport)
thread1.start()
thread2.start()

