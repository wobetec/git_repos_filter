from modules.query import Query
from modules.search import Search
from modules.results import Result
from modules.interface import interface

import json

class App():

    def __init__(self):
        self.results = {}
        self.query = None
        self.search = Search()
        self.interface = interface.GraphicsInterface()



    def begin(self):
        self.query, self.results = self.openCache()
        self.interface.title()


    def run(self):
        self.interface.clearScreen()
        self.interface.queryShow(self.query)
        print("")
        self.interface.resultsShow(self.returnResults())
        print("")
        command = self.interface.commandLine()
        
    
    def returnResults(self):
        return list(self.results.keys())


    def openCache(self):
        with open("./cache/cache.json", "r") as f:
            file = json.load(f)
        
        query = Query(
                    keywords = file["query"]["keywords"],
                    parameters = file["query"]["parameters"],
                    pag_count = file["query"]["pag_count"], 
                    all_pages = file["query"]["all_pages"], 
                    more_filters = file["query"]["more_filters"],
                    others = file["query"]["others"]
                )
        
        results = file["results"]

        return query, results


    def saveCache(self):
        query = self.query.toCache()

        dic = {"query":query, "results":self.results}

        with open("./cache/cache.json", "w") as f:
            f.write(json.dumps(dic, indent=4))


if __name__ == "__main__":
    app = App()
    app.begin()
    while True:
        app.run()
        pass

    app.end()


