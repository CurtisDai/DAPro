import socket
import threading
import json
import Log
from Log import report as Log_report
#from Suzuki_Kasami_Alg.NodeProg import NodeProg
from NodeProg import NodeProg

class MainNode(object):

    def __init__(self,host,port):
        # My socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.bind((host, port))

        # Server info
        # serverip = input('aim address:')
        # serverport = int(input('aim port:'))
        serverip = '169.254.213.193'
        serverport = 6000
        self._serveraddr = (serverip, serverport)

        # Create suziki node
        self._SuzukiNode = NodeProg(None, myaddr, port + 1)

        # The address of critical section
        self._cs_addr = [None]

        # Init server listener
        self._serverListener = ServerListener(self._s,self._SuzukiNode,self._cs_addr)
        self._serverListener.start()

        # Set the server address inside Log
        Log.LOG_SERVERADDR = self._serveraddr

        self._listening = False


    def run(self):
        self._listening = True
        while self._listening:

        	print("\n===========================================")
            print("what you wanna do now?(reply the number)")
            print("1. login")
            print("2. go to storehouse")
            print("3. exit")
        	print("===========================================\n")

            # DONT KNOW WHY
            i = input(">>> ")
            if i == '':
                continue
            num = int(i)
            if num == 1:
                password = input("Your password >>> ")
                msg = {"head": "login", "password": password}
                data = json.dumps(msg)
                self._s.sendto(data.encode(), self._serveraddr)  # send
            elif num == 2:
                # ship = input('aim address:')
                # shport = int(input('aim port:'))
                # shaddr = (ship, shport)
                msg = {"head": "givemoney","id":self._SuzukiNode.getId()}
                data = json.dumps(msg)
                data = data.encode()
                # request token before enter cs
                if self._SuzukiNode.getId() is not None:
                    assert isinstance(self._SuzukiNode,NodeProg)

                    if self._SuzukiNode.csEnter():
                        Log_report('enter', True,self._SuzukiNode.getId())
                        self._s.sendto(data, self._cs_addr[0])  # send
                    # else:
                    #     s.sendto(json.dumps(report('request', True)), serveraddr)
                    else:
                        print("Waiting")
                else:
                    print("You haven't login")
            elif num == 3:
                self._SuzukiNode.close()
                self.close()
            else:
                print("not offer this service now")


    def close(self):
        self._listening = False

class ServerListener(threading.Thread):
    def __init__(self,socket,sknode,csaddr):
        threading.Thread.__init__(self)
        self._listening = True
        self._s = socket
        self._SKNode = sknode
        self._csaddr = csaddr

        # put the cs_addr outside the algorithm
    def receive_message(self,data):

        if data['head'] == 'initialize':
            self._SKNode.start()
            content = data['content']

            # update Log.LOD_ID here
            nodeList = content['allnodes']

            ownToken = content['ownToken']
            sid = content['id']
            self._SKNode.createListenerToServer(sid)
            # Seperate CS and other nodes
            nList = []
            for node in nodeList:
                id, addr = node
                if id == 'CS':
                    tmpip, tmpport = addr
                    self._csaddr[0] = (tmpip, tmpport)
                else:
                    nList.append(node)
            self._SKNode.updateNodesInfo(nList)
            if ownToken == True:
                self._SKNode.initTokenUponServer()
            print("[Login] Successfully")

            # TODO] server message haven't include cs address content -> handled above
            # cs_addr = data['cs_addr']

            # TODO] LET SERVER RECORD BEFORE SEND OWNTOKExN

        elif data['head'] == 'update':
            if self._SKNode is not None:
                node = data['content']
                self._SKNode.updateNewNodeInfo([node])
                print("[Update] My list upon new node")
            else:
                print("[You have not login]")

        elif data['head'] == 'money' or data['head'] == 'decline':
            if data['head'] == 'money':
                m = data['content']
                print("You have got the money: " + str(m))
            elif data['head'] == 'decline':
                print("Fail to receive money")

            feedback = self._SKNode.csLeave()
            if feedback == False:
                print('No one need the token,Let me hold')

                # TODO] REPORT TO MONITOR
                Log_report('leave', True, self._SKNode.getId())

            elif feedback == None:
                print("I need a token")
            else:
                feed, id = feedback
                print("Token have been passed")

                # TODO] REPORT TO MONITOR
                Log_report('pass', id, self._SKNode.getId())
        else:
            pass

    def run(self):
        print('start listening\r\n')
        while self._listening:
            msg, addr = self._s.recvfrom(2048)  # receive
            print('\nreceive from' + str(addr) + ':\n\t' + msg.decode() + '\n:')


            data = json.loads(msg.decode())

            # Client handling all the receiving messages
            output = self.receive_message(data)
            # output = json.dumps(output)
            # s.sendto(output,serveraddr)

    def close(self):
        self._listening = False
        self._s.close()



if __name__ == '__main__':
    host = socket.gethostname()
    myaddr = socket.gethostbyname(host)
    print('logger ip address:', myaddr)
    port = int(input('your port:'))

    MainNode(host,port).run()