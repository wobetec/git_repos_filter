class Parser():

    def __init__(self):
        self.tree = None
        pass


    def getPath(self, string):
        splited = string.split(" ")

        insideArg = False
        pathList = []
        args = {}
        lastArg = None

        for piece in splited:
            if len(piece) == 0:
                continue
            if not insideArg and piece[0]!="-":
                pathList.append(piece)
            elif piece[0]=="-":
                insideArg = True
                lastArg = piece
                args[lastArg] = []
            elif insideArg:
                args[lastArg].append(piece)
        
        pathList.reverse()
        path = {"arguments":args}
        for directory in pathList:
            new_dic = {directory:path.copy()}
            path = new_dic.copy()
        
        return path


    def checkPath(self, path):
        validPath = True
        validArgs = True

        treeSlice = self.tree.copy()
        pathSlice = path.copy()

        while True:
            now = list(pathSlice.keys())[0]
            if now != "arguments":
                try:
                    treeSlice = treeSlice[now]
                except KeyError:
                    validPath = False
                    break
                pathSlice = pathSlice[now]
            else:
                treeSlice = treeSlice[now] #args
                pathSlice = pathSlice[now] #args

                dicCalls = {}
                for arg in treeSlice.keys():
                    calls = treeSlice[arg]["calls"]
                    for call in calls:
                        dicCalls[call] = arg

                for key in treeSlice.keys():
                    if treeSlice[key]["must"]:
                        try:
                            name = None
                            for i in treeSlice[key]["calls"]:
                                try:
                                    name = pathSlice[i]
                                except KeyError:
                                    continue
                            if name == None:
                                validArgs = False
                                break
                            elif not treeSlice[key]["validator"](name):
                                validArgs = False
                                break
                        except KeyError:
                            validArgs = False
                            break
                break
                    
        return validPath and validArgs
   

    def getArguments(self, path):
        treeSlice = self.tree.copy()
        pathSlice = path.copy()
        do = None

        while True:
            now = list(pathSlice.keys())[0]
            if now != "arguments":
                treeSlice = treeSlice[now]
                pathSlice = pathSlice[now]
                last = now
            else:
                break

        #Get arguments
        treeSlice = treeSlice["arguments"]
        pathSlice = pathSlice["arguments"]

        arguments = {}

        for arg in treeSlice.keys():
            callValue = None
            for i in treeSlice[arg]["calls"]:
                try:
                    callValue = pathSlice[i]
                    break
                except KeyError:
                    continue
            if callValue == None:
                arguments[arg] = treeSlice[arg]["default"]
            else:
                arguments[arg] = callValue
            
        return arguments

    
    def getDo(self, path):
        treeSlice = self.tree.copy()
        pathSlice = path.copy()
        do = None
        while True:
            now = list(pathSlice.keys())[0]
            if now != "arguments":
                treeSlice = treeSlice[now]
                pathSlice = pathSlice[now]
                last = now
            else:
                do = treeSlice["do"]
                break
        return do

