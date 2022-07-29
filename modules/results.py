import json
import pandas as pd
from datetime import datetime

class Result():

    def __init__(self, search):
        self.metadata = search.metadata
        self.jsonOriginal = search.response
        self.manipulated = self.jsonOriginal


    #######################-->Sort<--#######################
    def sortByStars(self):
        nodes = self.jsonOriginal["data"]["search"]["nodes"]
        new_list = sorted(nodes, key=lambda node: node["stargazers"]["totalCount"], reverse=True)
        self.manipulated["data"]["search"]["nodes"] = new_list
        self.metadata["Criterio de separacao"] =  "stars"


    #####################-->Slicing<--#####################
    def sliceFirsts(self, n):
        nodes = self.manipulated["data"]["search"]["nodes"]
        self.manipulated["data"]["search"]["nodes"] = nodes[:n]
        self.metadata["Utilizados"] = n


    #####################-->Return<--######################
    def toJson(self, filePath, metadata = True):
        if metadata:
            self.manipulated["data"]["search"]["metadata"] = self.metadata
            
        with open(filePath, "w") as f:
            f.write(json.dumps(self.manipulated, indent=4))


    def toExcel(self, filePath, itens = ["name", "url", "star"], metadata = True):

        dic = self.manipulated["data"]["search"]["nodes"]
        lista = [[item["name"], item["url"], item["stargazers"]["totalCount"]] for item in dic]
        df = pd.DataFrame(lista, columns=itens)

        if metadata:
            coluns = ["keywords-include", "keywords-exclude", "parameters-include", "parameters-exclude", "Total", "Utilizados", "Data", "Criterio de separacao", ]
            data = [self.metadata["keywords-include"], self.metadata["keywords-exclude"], self.metadata["parameters-include"], self.metadata["parameters-exclude"], self.metadata["Total"], self.metadata["Utilizados"], self.metadata["Data"], self.metadata["Criterio de separacao"]]
            lista = [tuple(data)]
            dfM = pd.DataFrame(lista, columns=coluns)
            
        writer = pd.ExcelWriter(filePath, engine="openpyxl")
        df.to_excel(writer, "Repositories", index=False)
        dfM.to_excel(writer, "Metadata", index=False)

        writer.save()


    

