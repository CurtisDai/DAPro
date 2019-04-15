from NodeList import NodeList
from TokenInfo import TokenInfo
from NodeListener import NodeListener
from NodeInfo import NodeInfo
from MessageType import MessageType
from Token import Token
from Request import Request
from Log import *
import socket
import time
from threading import Thread
import sys

class NodeProg:

    def __init__(self,id,serverIp,serverPort,nodeIp,nodePort):
        #Thread.__init__(self)

        # The information maintained of other node
        self._RequestNumber = {} # the RN is a dictionary with entry (id:reqNum)
        # Constains all the node info except from itself
        self._AllNodeInfo = NodeList()

        # The token info hold by this Node
        self._tokenInfo = TokenInfo()
        self._token = []

        # The infomation of this Node
        self._id = id
        self._ip = nodeIp
        self._port = nodePort
        self._serverIp = serverIp
        self._serverPort = serverPort
        self._seqNum = 0

        #self._requestMade = False

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #info dict
        self._info = {
            "rn": self._RequestNumber,
            "tokInfo": self._tokenInfo,
            "seq": self._seqNum,
            "id": self._id,
            "tok": self._token
        }

    def run(self):

        # Start listening to server first
        self._createListenerToServer(self._serverIp,self._serverPort)


        # TODO] Set selfId by receiving from server
        #self._id = id

        # Start listening to all nodes
        self._Listeners = None
        self._createListenerToAll()

    # This listener should update the AllNodeInfo List
    def _createListenerToServer(self,serverIp,serverPort):
        # TODO] Set the fixed server address

        # [Testing by simply read from file]

        import configparser
        from NodeInfo import NodeInfo
        config = configparser.ConfigParser()
        config.read('Config.ini')
        num = config['default']['num']
        nodes = config['nodes']
        for key in nodes:
            if key != self._id:
                ip,port = nodes[key].split(":")
                self._AllNodeInfo.addNode(NodeInfo(key,ip,port))
            else:
                ip, port = nodes[key].split(":")
                self._ip = ip
                self._port = port

        # Initialize all the seq number
        for key in nodes:
            self._RequestNumber[key] = 0

        # Initial the token if id is aa
        if self._id == 'aa':
            self._token.append(Token())
            self._token[0].createFromList(self._AllNodeInfo)
            self._tokenInfo.changeMode(hasToken=True)

    # Actually we need only one listener for listening all the other nodes
    def _createListenerToAll(self):
        self._Listeners = NodeListener((self._ip,self._port),self._info)
        self._Listeners.start()

    # def gotToken(self):
    #     return self._token.gotToken()

    def request(self):
        self._seqNum += 1
        self._requestMade = True
        self._RequestNumber[self._id] = self._seqNum

        msg = MessageType()
        req = msg.genRequest(self._id,self._seqNum)
        sendLOG(SENDREQ, "Broadcast")

        # Broadcast the request message
        for node in self._AllNodeInfo.getAllNodes():
            assert isinstance(node, NodeInfo)
            self._socket.sendto(req,(node.getHost(),node.getPort()))

    def csEnter(self):
        if self._tokenInfo.gotToken() and self._token[0].isEmpty():
            self._tokenInfo.changeMode(tokenInUse=True)
            return True
        else:
            if self._tokenInfo.gotToken() and not self._token[0].isEmpty():
                ele = self._token[0].popQueue()
                self._sendToken(ele.getId())

            if not self._tokenInfo.gotToken():
                self.request()
                notifyLOG(WAITTOK)

                # Pause for a little while
                counter = 0
                sys.stdout.write('[Waiting ')
                while not self._tokenInfo.gotToken() and counter < 50:
                    counter += 1
                    time.sleep(0.1)
                    # Simple progress bar showing wait status
                    sys.stdout.write('.')
                    sys.stdout.flush()
                sys.stdout.write('\n')
                sys.stdout.flush()

                if self._tokenInfo.gotToken():
                    notifyLOG(TOKENRECV)
                    self._tokenInfo.changeMode(tokenInUse=True)
                    return True
                else:
                    notifyLOG(TIMEOUT)
                    self._seqNum -= 1
                    self._RequestNumber[self._id] = self._seqNum
                    return False

    def csLeave(self):
        assert isinstance(self._token[0],Token)

        # TODO] CHECK THIS
        if self._tokenInfo.gotToken():
            if self._tokenInfo.usingToken():
                self._token[0].modifyLastRequest(self._id,self._seqNum)
            # self._requestMade = False

        if self._tokenInfo.gotToken():
            self._tokenInfo.changeMode(tokenInUse=False)
            for id, reqNum in self._RequestNumber.items():
                if id != self._id and reqNum == self._token[0].getReqNum(id) + 1:
                    self._token[0].letQueue(Request(id, reqNum))

            tResult = self._token[0].popQueue()
            if tResult is None:
                return False
            else:
                if not self._sendToken(tResult.getId()):
                    return False
                return True
        else:
            return False

    def holdAndWait(self):
        while self._tokenInfo.gotToken() and not self._tokenInfo.usingToken():
            pop = self._token[0].popQueue()
            if pop is None:
                time.sleep(0.5)
                continue
            else:
                self._sendToken(pop.getId())
                self._tokenInfo.changeMode(hasToken=False)

    def letMeIn(self):
        if self._tokenInfo.gotToken():
            self._tokenInfo.changeMode(tokenInUse= True)

    def _sendToken(self,id):
        msg = MessageType()
        data = msg.genToken(self._token[0],self._id)

        nodeInfo = self._AllNodeInfo.getNode(id)
        sendLOG(SENDTOK, nodeInfo.getHost() +':'+ str(nodeInfo.getPort()))
        try:
            self._socket.sendto(data, (nodeInfo.getHost(), nodeInfo.getPort()))
            self._tokenInfo.changeMode(hasToken=False,tokenInUse=False)
            # make the self._token to be [], not pop the queue
            self._token.pop(0)
        except Exception as e:
            print(e)
            return False
        return True

    def close(self):
        self._socket.close()
        self._token = None

        # Close the server listener

        # Close node listener
        if self._Listeners is not None:
            self._Listeners.close()

def usage():
    pass


