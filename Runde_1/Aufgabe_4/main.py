cuboidHeight: int = 2
cuboidDepth: int = 2
cuboidWidth: int = 2

class Node:
    def __init__(self, nodeID: int) -> None:
        self.nodeID: int = nodeID
        self.peerNodes: list = []
    
    def __str__(self) -> str:
        return "NodeID: {0}, Connections: {1}".format(self.nodeID, ' '.join((str(e)).__add__(',') for e in self.peerNodes))

class UnitCube:
    def __init__(self, qubeID: int) -> None:
        self.cubeID: int = qubeID
        self.cubeNodes: list = []
    
    def __str__(self) -> str:
        return "QubeID: {0}, QubeNodes: {1}".format(self.cubeID, ' '.join((str(e)).__add__(',') for e in self.cubeNodes))



nodeListRaw: list[Node] = []
nodeList: list[list[list[int]]] = []
cubeList: list[UnitCube] = []

nodeHashmapTable: list[list] = []

nodeDontWorkPaths: list = []
nodeWorkPaths: list = []

nodeConnectionCounter = 0

test: dict = {'tst': 1}

def initiateNodeList() -> None:
    nodeIDCounter = 0
    for i in range(cuboidHeight+1):
        nodeList.append([])
        for j in range(cuboidDepth+1):
            nodeList[i].append([])
            
            for _ in range(cuboidWidth+1):
                nodeList[i][j].append(nodeIDCounter)
                nodeListRaw.append(Node(nodeIDCounter))
                nodeIDCounter += 1

def createcubeList() -> None:
    for _ in range(cuboidHeight*cuboidDepth*cuboidWidth):
        unitCubeObj = UnitCube(_)

        # Add the 8 Nodes to each unit qube!!!
        cubeList.append(unitCubeObj)

    
    qubeIDCounter = 0
    for i in range(cuboidHeight):
        for j in range(cuboidDepth):
            for k in range(cuboidWidth):
                qubeObj = cubeList[qubeIDCounter]
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i][j][k]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i][j][k+1]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i][j+1][k]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i][j+1][k+1]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i+1][j][k]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i+1][j][k+1]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i+1][j+1][k]].nodeID)
                qubeObj.cubeNodes.append(nodeListRaw[nodeList[i+1][j+1][k+1]].nodeID)
                qubeIDCounter += 1

def findPeerNodesOfNode() -> None:
    global nodeConnectionCounter
    global nodeHashmapTable

    for i in nodeListRaw:
        print("Node: {0}".format(str(i.nodeID+1)))
        for j in cubeList:
            if i.nodeID in j.cubeNodes:
                i.peerNodes.append(j.cubeNodes[len(j.cubeNodes)-1-j.cubeNodes.index(i.nodeID)])
                nodeConnectionCounter += 1
        nodeHashmapTable.append([])
        for e in i.peerNodes:
            nodeHashmapTable[len(nodeHashmapTable)-1].append(e)

usedPeerNodes: list[list] = []

# def searchForPeerNodes(originNode, curNode) -> bool:
#     peerCounter = 0
#     for i in nodeListRaw[curNode].peerNodes:
#         if i not in usedPeerNodes:
#             usedPeerNodes[originNode].append(i)
#             peerCounter += 1
#             result = searchForPeerNodes(originNode, i)
#             if result == True:
#                 usedPeerNodes[originNode].append(i)

#     if peerCounter == 0:
#         return False
#     else:
#         return True




def brutforceOnePossibilitie() -> None:
    global usedPeerNodes
    currentHashmapPath: list = []

    isNotPossibilitieFound = True
    for i in nodeListRaw:
        currentHashmapPath = []
        copyNodeMap = nodeHashmapTable
        currentNodeCounter = i.nodeID
        while isNotPossibilitieFound:
            isEntityFound = False
            entityCounter = 0
            usedPeerNodes.append([])
            while not isEntityFound:
                currentHashmapPath.append()
                # if entityCounter < len(nodeHashmapTable):
                #     entityNodeHash = nodeHashmapTable[entityCounter]
                #     if entityNodeHash[0] == currentNodeCounter:
                #         isEntityFound = True
                #         usedPeerNodes[entityCounter].append(currentNodeCounter)
                #         currentNodeCounter = entityNodeHash[1]
                # else:
                #     break
                # entityCounter += 1
            
            if not isEntityFound:
                break

def checkIfAllNodesUsed(copy: list) -> bool:
    nodesPerCube = []
    for k in cubeList:
        nodesPerCube.append([])
    
    for i, _ in enumerate(copy):
        for j, v in enumerate(cubeList):
            if i in v.cubeNodes and len(_) != 0:
                nodesPerCube[j].append(i)
    
    cubeCounter = 0
    for x in nodesPerCube:
        if len(x) < 7:
            cubeCounter += 1
    
    if cubeCounter == len(cubeList):
        return True
    else:
        return False


def brutforceAlgorithm() -> None:
    global usedPeerNodes
    currentHashmapPath: list = []

    for i in nodeListRaw:
        currentHashmapPath = []
        copyNodeMap = nodeHashmapTable
        isPossibilitieFound = False
        currentNodeID = i.nodeID
        currentHashmapPath.append(0)
        prevousNodeID = 0
        while not isPossibilitieFound:

            if len(copyNodeMap[currentHashmapPath[len(currentHashmapPath)-1]]) > 0:
                for ind, val in enumerate(copyNodeMap[currentNodeID]):
                    if val == prevousNodeID:
                        copyNodeMap[currentNodeID].remove(prevousNodeID)
                        if len(copyNodeMap[currentNodeID]) == 1:
                            currentHashmapPath.__delitem__(len(currentHashmapPath)-1)
                        currentNodeID = prevousNodeID
                    elif len(copyNodeMap[val]) == 0:
                        result = checkIfAllNodesUsed(copyNodeMap)
                        if result == True:
                            print("Found End")
                            print("-------")
                            print(currentHashmapPath)
                            print("-------")
                        else:
                            print("Not all Cubes were used")
                            print("-------")
                            print(currentHashmapPath)
                            print("-------")
                        currentNodeID = currentHashmapPath[len(currentHashmapPath)-2+1]
                    else:
                        # currentHashmapPath[len(currentHashmapPath)-1] = ind
                        currentHashmapPath.append(val)
                        copyNodeMap[currentNodeID].remove(val)
                        prevousNodeID = currentNodeID
                        currentNodeID = val
                        print(copyNodeMap)
                        break
            else:
                pass
                # currentHashmapPath.__delitem__(len(currentHashmapPath-1))
                # currentHashmapPath[len(currentHashmapPath)-1] += 1
        

# def brutforceAllPossibilities() -> None:
#     for i in nodeListRaw:
#         getPeerNode()


if __name__=='__main__':
    initiateNodeList()
    for i in range(cuboidHeight+1):
        print("Ebene "+str(i))
        for j in range(cuboidDepth+1):
            print("Tiefe "+str(j))
            for k in range(cuboidWidth+1):
                print(nodeListRaw[nodeList[i][j][k]].nodeID)

    print('\n')

    createcubeList()

    for j in range(len(cubeList)):
        print(cubeList[j].__str__())

    print('\n')

    findPeerNodesOfNode()

    for k in nodeListRaw:
        print(k.__str__())
    

    brutforceAlgorithm()

    print('\n')

    print("Total amount of unit cubes: {0}".format(len(cubeList)))
    print("Total amount of nodes: {0}".format(len(nodeListRaw)))
    print("Total amount of node connections: {0}".format(str(nodeConnectionCounter)))