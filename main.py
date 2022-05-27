from sre_compile import isstring
from modules.query import Query
from modules.search import Search
from modules.results import Result
from modules.interface import interface
from modules.interface import inquirer as inq
from modules.cliparser.parser import Parser

import json

class App():

    def __init__(self):
        self.results = {"empity_1": {}, "empity_2": {}, "empity_3": {}, "empity_4": {}, "empity_5": {}}
        self.query = None
        self.search = Search()
        self.interface = interface.GraphicsInterface() 
        self.parser = self.Proxy()
        self.running = True


    def begin(self, begin=True):
        self.query, self.results = self.openCache()
        self.interface.title(begin)


    def run(self):
        self.interface.clearScreen()
        self.interface.queryShow(self.query)
        print("")
        self.interface.resultsShow(self.returnResults())
        print("")
        command = self.interface.commandLine()
        return command
        
    
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
        results = {x:(Result(dic=file["results"][x]) if file["results"][x] != {} else Result()) for x in file["results"].keys()}

        return query, results


    def saveCache(self):
        query = self.query.toCache()
        saveResults = {x:self.results[x].toJsonCache() for x in self.results.keys()}

        dic = {"query":query, "results":saveResults}

        with open("./cache/cache.json", "w") as f:
            f.write(json.dumps(dic, indent=4))


    def end(self):
        self.saveCache()
        self.interface.title(begin=False)

    ####################-->query<--######################
    def do_edit(self, arguments):
        print(arguments)
        if arguments["fields"] == "all":
            self.interface.clearScreen()
            new_query = inq.query.run(placeholder = self.query.getInq())
            print(new_query)
            self.query.changeInq(new_query)
        
    
    ####################-->search<--######################
    def do_do(self, arguments):
        self.search.get_search(self.query)
        name, slot = arguments["name"][0], arguments["slot"][0]
        self.results.pop(slot)
        result_temp = Result(search = self.search)
        self.results[name] = result_temp
    
    
    ####################-->results<--######################
    def do_see(self, arguments):
        self.interface.clearScreen()
        self.interface.showResult(self.results[arguments["slot"][0]])
        pass

    ####################-->quit<--######################
    def do_finish(self):
        self.running = False
    
    class Proxy(Parser):

        original_tree = {
            "query":{
                "type":"class",
                "edit":{
                    "type":"function",
                    "arguments":{
                        "fields":{
                            "calls":["-f", "--field"],
                            "must":False,
                            "type":"str",
                            "default":"all",
                            "validator":None
                        }
                    },
                    "do": lambda x, y: x.do_edit(y),
                }
            },
            "search":{
                "type":"class",
                "do":{
                    "type":"function",
                    "arguments":{
                        "name":{
                            "calls":["-n", "--name"],
                            "must":True,
                            "type":"str",
                            "default": None,
                            "validator": lambda x: type(x[0]) == type("str"),
                        },
                        "slot":{
                            "calls":["-s", "--slot"],
                            "must":True,
                            "type":"str",
                            "default": None,
                            "validator": lambda x: type(x[0]) == type("str"),
                        },
                    },
                    "do": lambda x, y: x.do_do(y),
                }
            },
            "results":{
                "type":"class",
                "see":{
                    "type":"function",
                    "arguments":{
                        "slot":{
                            "calls":["-s", "--slot"],
                            "must":True,
                            "type":"str",
                            "default": None,
                            "validator": lambda x: type(x[0]) == type("str"),
                        },
                        "detail-level":{
                            "calls":["-d", "--detail-level"],
                            "must":False,
                            "type": "int",
                            "default": 1,
                            "validator": lambda x: type(x[0]) == type(0),
                        },
                    },
                    "do": lambda x, y: x.do_see(y),
                },
            },
            "quit":{
                "type":"function",
                "arguments": {},
                "do": lambda x, y: x.do_finish()
                }
        
        }

        def __init__(self):
            self.tree = App.Proxy.original_tree


if __name__ == "__main__":
    app = App()
    app.begin()
    while app.running:
        command = app.run()
        path = app.parser.getPath(command)
        if app.parser.checkPath(path):
            arguments = app.parser.getArguments(path)
            app.parser.getDo(path)(app, arguments)
    app.end()

