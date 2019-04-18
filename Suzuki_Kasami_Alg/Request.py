class Request:

    def __init__(self,id,seq=0):
        self._id = id
        self._seqNum = seq

    def getId(self):
        return self._id

    def getSeq(self):
        return self._seqNum

    def setId(self,id):
        self._id = id

    def setReq(self,req):
        self._seqNum = req