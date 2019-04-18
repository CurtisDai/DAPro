class TokenInfo:

    def __init__(self):
        self._hasToken = False
        self._tokenInUse = False
        self._tokenRecvd = False

    def changeMode(self,hasToken=None,tokenInUse=None,tokenRecvd=None):
        if hasToken is not None:
            self._hasToken = hasToken
        if tokenInUse is not None:
            self._tokenInUse = tokenInUse
        if tokenRecvd is not None:
            self._tokenRecvd = tokenRecvd

    def gotToken(self):
        return self._hasToken

    def usingToken(self):
        return self._tokenInUse

    def recvdToken(self):
        return self._tokenRecvd