
import pandas as pd
from modules.query import Query
from modules.search import Search


if __name__ == "__main__":
    s = Search()

    keywords = {"include":["bioinformatics"], "exclude":[]}
    parameters = {"include":{"language":"python"}, "exclude":{}}

    query = Query(keywords, parameters, pag_count=1, all_pages = False)
    s.get_search(query)

    try:
        print(s.response["data"]["search"]["repositoryCount"])
    except:
        pass
    pass

    #s.sort_repos_stars() #ordena a busca por stars
    #s.get_firsts(100) #pega apenas os n primieros da busca
    #s.to_excel() #salva a busca em um .xlsx

