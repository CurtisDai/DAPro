from NodeList import NodeList
from queue import Queue
from Request import Request


class Token:

    def __init__(self):
        self._LastRequestNumber = None
        self._Queue = None
        self._QueueIds = None

    def createFromList(self,nodelist):
        if isinstance(nodelist,NodeList):
            lst = nodelist.getNodeIDs()
            self._LastRequestNumber = {}
            for id in lst:
                self._LastRequestNumber[id] = 0
        else:
            raise ValueError("The nodeList is invalid")
        self._Queue = []
        self._QueueIds = set()

    def createFromMsg(self,queue,reqNum):
        self._LastRequestNumber = reqNum
        self._Queue = queue
        self._QueueIds = set()
        for ele in self._Queue:
            assert isinstance(ele, Request)
            self._QueueIds.add(ele.getId())


    def getReqList(self):
        return self._LastRequestNumber

    def getReqNum(self,id):
        return self._LastRequestNumber[id]

    def setReqNum(self,reqNum):
        self._LastRequestNumber = reqNum

    def getQueue(self):
        return self._Queue

    def setQueue(self,q):
        self._Queue = q

    def isEmpty(self):
        return len(self._Queue) == 0

    def popQueue(self):
        if self._Queue is None:
            return None
        if len(self._Queue) == 0:
            return None

        ele = self._Queue.pop(0)
        self._QueueIds.remove(ele.getId())
        return ele


    def letQueue(self,request):

        assert isinstance(request,Request)
        if self._Queue is not None:
            if request.getId() not in self._QueueIds:
                self._Queue.append(request)
                self._QueueIds.add(request.getId())

    def modifyLastRequest(self,id,req):
        self._LastRequestNumber[id] = req