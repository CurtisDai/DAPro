from NodeInfo import NodeInfo

class NodeList:

    def __init__(self):
        self._nodeList = None

    def getCount(self):
        if self._nodeList is not None:
            return len(self._nodeList)
        else:
            raise ValueError("The None List haven't been initialized")

    def getNode(self,id):
        if self._nodeList is not None:
            return self._nodeList[id]

    def addNode(self,node):
        assert isinstance(node,NodeInfo)

        if self._nodeList is not None:
            if self._nodeList.get(node.getId()) is not None:
                print("[Warning | Modifying node]: ",node.getId())
        else:
            self._nodeList = {}

        self._nodeList[node.getId()] = node

    def deletNode(self,node):
        assert isinstance(node, NodeInfo)

        if self._nodeList is not None:
            self._nodeList.pop(node.getId())

    def handling(self,nodeList):
        # add the method to handle all the receiving node list
        for node in nodeList:
            self.addNode(node)

    # Return a list of Node Object
    def getAllNodes(self):
        lst = []
        if self._nodeList is not None:
            for ele in self._nodeList.values():
                lst.append(ele)
        return lst

    def getNodeIDs(self):
        if self._nodeList is not None:
            return self._nodeList.keys()
        else:
            raise ValueError("The None List haven't been initialized")