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
                print("[Warning | Modifying existed node]: ",node.getId())
                return False
            else:
                self._nodeList[node.getId()] = node
                return True
        else:
            self._nodeList = {}
            self._nodeList[node.getId()] = node
            return True

    # update the NodeList when parameter is a list of addr in the form of
    def updatefromAddrList(self,list):
        newNodes = []
        for ele in list:
            # all the update node info are in the form of [id,[ip,port]]
            id,addr = ele
            ip,port = addr
            node = NodeInfo(id,ip,port)
            r = self.addNode(node)
            if r:
                newNodes.append(id)
        return newNodes


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
            return []