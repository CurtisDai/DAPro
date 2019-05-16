from NodeList import NodeList
from TokenInfo import TokenInfo
from NodeListener import NodeListener
from NodeInfo import NodeInfo
from MessageType import MessageType
from Token import Token
from Request import Request
from Log import *
from Log import report as Log_report
import socket
import time
from threading import Thread
import sys


class NodeProg(Thread):

    def __init__(self,sock,nodeIp,nodePort):
        Thread.__init__(self)

        # The information maintained of other node
        self._RequestNumber = {} # the RN is a dictionary with entry (id:reqNum)
        # Constains all the node info except from itself
        self._AllNodeInfo = NodeList()

        # The token info hold by this Node
        self._tokenInfo = TokenInfo()
        self._token = []

        # The infomation of this Node
        self._id = None
        self._ip = nodeIp
        self._port = nodePort

        #self._serverIp = serverIp
        #self._serverPort = serverPort
        self._seqNum = 0

        #self._requestMade = False

        if sock is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.bind((self._ip, self._port))
        else:
            self._socket = sock

        #info dict
        self._info = {
            "rn": self._RequestNumber,
            "tokInfo": self._tokenInfo,
            "seq": self._seqNum,
            "id": self._id,
            "tok": self._token,
            "all":self._AllNodeInfo
        }

        self._Listeners = None

    def run(self):

        # Start listening to server first [Not need for actual scenario]
        #self._createListenerToServer()

        # Start listening to all nodes
        self._createListenerToAll()

    # This listener should update the AllNodeInfo List
    def createListenerToServer(self,id):

        # # [Testing by simply read from file]
        # import configparser
        # from NodeInfo import NodeInfo
        # config = configparser.ConfigParser()
        # config.read('Config.ini')
        # num = config['default']['num']
        # nodes = config['nodes']
        # for key in nodes:
        #     if key != self._id:
        #         ip,port = nodes[key].split(":")
        #         self._AllNodeInfo.addNode(NodeInfo(key,ip,port))
        #     else:
        #         ip, port = nodes[key].split(":")
        #         self._ip = ip
        #         self._port = port
        #
        # # Initialize all the seq number
        # for key in nodes:
        #     self._RequestNumber[key] = 0
        #
        # if self._id == 'aa':
        #     self.initTokenUponServer()
        # # [Testing by simply read from file]

        self._id = id
        self._info['id'] = id

    def updateNodesInfo(self,lst):
        newNodes = self._AllNodeInfo.updatefromAddrList(lst)
        for id in newNodes:
            self._RequestNumber[id] = 0

    def updateNewNodeInfo(self,lst):
        newNodes = self._AllNodeInfo.updatefromAddrList(lst)
        for id in newNodes:
            self._RequestNumber[id] = 0
            if self._tokenInfo.gotToken():
                self._token[0].modifyLastRequest(id,0)

    def initTokenUponServer(self):
        # Initial the token if server aprrove
        self._token.append(Token())
        self._token[0].createFromList(self._AllNodeInfo)
        self._tokenInfo.changeMode(hasToken=True)

    # Actually we need only one listener for listening all the other nodes
    def _createListenerToAll(self):
        self._Listeners = NodeListener(self._socket,(self._ip,self._port),self._info)
        self._Listeners.start()

    # def gotToken(self):
    #     return self._token.gotToken()

    def request(self):
        self._seqNum += 1
        self._info['seq'] += 1
        self._requestMade = True
        self._RequestNumber[self._id] = self._seqNum

        msg = MessageType()
        req = msg.genRequest(self._id,self._seqNum)
        sendLOG(SENDREQ, "Broadcast")

        # Broadcast the request message except for self
        for node in self._AllNodeInfo.getAllNodes():
            if node.getId() != self._id:
                assert isinstance(node, NodeInfo)
                self._socket.sendto(req,(node.getHost(),node.getPort()))

    def csEnter(self):
        if self._tokenInfo.gotToken() and self._token[0].isEmpty():
            self._tokenInfo.changeMode(tokenInUse=True)
            return True
        else:
            if not self._tokenInfo.gotToken():

                # TODO] REPORT TO MONITOR
                Log_report('request', True, self._info['id'])
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

                    # TODO] REPORT TO MONITOR
                    #Log_report('token', True, self._info['id'])
                    self._tokenInfo.changeMode(tokenInUse=True)
                    return True
                else:
                    notifyLOG(TIMEOUT)
                    self._seqNum -= 1
                    self._info['seq'] -= 1
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
                if not self._Listeners.sendToken(tResult.getId()):
                    return False
                return (True,tResult.getId())
        else:
            return None

    def close(self):
        # self._socket.close()
        self._tokenInfo.changeMode(False,False,False)
        self._token = []

        # Close the server listener

        # Close node listener
        if self._Listeners is not None:
            self._Listeners.close()

    def getId(self):
        return self._id


