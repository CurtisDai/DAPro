class NodeInfo:

    def __init__(self,id,host,port):
        self._id = id
        self._host = host
        if isinstance(port,str):
            self._port = int(port)

    def getId(self):
        return self._id

    def getHost(self):
        return self._host

    def getPort(self):
        return self._port