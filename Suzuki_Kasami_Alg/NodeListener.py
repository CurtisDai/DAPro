from threading import Thread
import socket
from MessageType import MessageType
from MessageType import REQUEST,TOKEN
from Log import *
from Token import Token

class NodeListener(Thread):

    def __init__(self,listenInfo,nodeInfo):
        Thread.__init__(self)
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        ip,port = listenInfo
        if isinstance(port,str):
            port = int(port)
        self._s.bind((ip,port))

        self._message = MessageType()
        self._info = nodeInfo
        self._close = False

    def run(self):
        while not self._close:
            data,addr = self._s.recvfrom(1024)
            validResult = self._message.parse(data)

            # handle when receiving error message
            if not validResult:
                listenerLOG(ERRORMSG,addr)
                continue

            # Handling request message
            if self._message.getType() == REQUEST:
                id = self._message.getContent()[0]
                seq = self._message.getContent()[1]
                listenerLOG(REQUESTMSG, addr,id)
                rn = self._info["rn"]

                if rn.get(id) is not None:
                    rn[id] = max(rn[id],seq)
                # In original paper, the queue is updated when node leave CS
                # tokInfo = self._info["tokInfo"]
                # if tokInfo.gotToken() and not tokInfo.usingToken():
                #     tok = self._info["tok"]
                #     if rn[id] == tok.getReqNum() + 1:

            # Handing token message
            elif self._message.getType() == TOKEN:
                tokInfo = self._info["tokInfo"]
                tok = self._info["tok"]
                tTok = self._message.getContent()
                id = self._message.getId()
                listenerLOG(TOKENMSG, addr,id)
                tok.append(tTok)
                tokInfo.changeMode(hasToken=True)


    def close(self):
        self._close = True
        self._s.close()

    def handlingData(self,data):
        pass

