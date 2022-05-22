from modules.query import Query
from modules.search import Search
from modules.results import Result


if __name__ == "__main__":
    s = Search()

    keywords = {"include":["bioinformatics"], "exclude":[]}
    parameters = {"include":{"language":"python"}, "exclude":{}}

    query = Query(keywords, parameters, pag_count=100, all_pages = False)
    
    s.get_search(query)
    r = Result(s)

    print(r.manipulated["data"]["search"]["repositoryCount"])
    r.toJson("./results/result.json")
    r.toExcel("./results/result.xlsx")



