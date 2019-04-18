import pickle
from Token import Token

REQUEST = 1
TOKEN = 2


class MessageType:

    def __init__(self):
        self._type = None
        self._content = None
        self._id = None

    def getId(self):
        return self._id

    def getType(self):
        return self._type

    def getContent(self):
        return self._content

    def genRequest(self,id,seq):
        content = {}
        content["type"] = REQUEST
        content["id"] = id
        content["seq"] = seq

        return pickle.dumps(content)

    def genToken(self,token,id):

        assert isinstance(token,Token)
        content = {}
        content["type"] = TOKEN
        content["id"] = id
        content["queue"] = token.getQueue()
        content["seq"] = token.getReqList()
        return pickle.dumps(content)

    def parse(self,obj):
        try:
            content = pickle.loads(obj)
        except:
            print("Undefined Message")
            return False

        if content["type"] == REQUEST:
            self._id = content["id"]
            self._type = content["type"]
            self._content = (content["id"],content["seq"])

        elif content["type"] == TOKEN:
            token = Token()
            token.createFromMsg(content["queue"],content["seq"])
            self._id = content["id"]
            self._type = content["type"]
            self._content = token
        return True



