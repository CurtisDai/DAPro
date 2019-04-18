from threading import Thread
import socket
from MessageType import MessageType
from MessageType import REQUEST,TOKEN
from Log import *
from Request import Request

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

                tokInfo = self._info['tokInfo']
                if tokInfo.gotToken() and not tokInfo.usingToken():
                    tok = self._info['tok'][0]
                    if tok.isEmpty() and rn[id] == tok.getReqNum(id) + 1:
                        self.sendToken(id)

            # Handing token message
            elif self._message.getType() == TOKEN:
                tokInfo = self._info["tokInfo"]
                tok = self._info["tok"]
                tTok = self._message.getContent()
                id = self._message.getId()
                listenerLOG(TOKENMSG, addr,id)
                tok.append(tTok)
                tokInfo.changeMode(hasToken=True)

    def sendToken(self,id):
        if not self._info['tokInfo'].gotToken() or self._info['tokInfo'].usingToken():
            return False

        msg = MessageType()
        data = msg.genToken(self._info['tok'][0],self._info['id'])

        nodeInfo = self._info['all'].getNode(id)
        sendLOG(SENDTOK, nodeInfo.getHost() +':'+ str(nodeInfo.getPort()))
        try:
            self._s.sendto(data, (nodeInfo.getHost(), nodeInfo.getPort()))
            self._info['tokInfo'].changeMode(hasToken=False,tokenInUse=False)
            # pop the self._token to be [], not pop the queue
            self._info['tok'].pop(0)
        except Exception as e:
            print(e)
            return False
        return True


    def close(self):
        self._close = True
        self._s.close()

    def handlingData(self,data):
        pass

