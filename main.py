from modules.query import Query
from modules.search import Search
from modules.results import Result

"""
#######################--> How to use <--#######################

1) Criar uma instância de Search que atua como buscador
    s = Search

2) Definir as keywor ds e os parameters a serem utilizados(keywords=list, parameters=dict)
    keywords = {"include":["bioinformatics"], "exclude":[]}
    parameters = {"include":{"language":"python"}, "exclude":{}}

3) criar uma instância de Query que criará a string a ser usada como query
    query = Query(keywords, parameters, pag_count=100, all_pages = False)

4) Realizar a busca usando a instância de Search e a de Query e armazenala em um resultado
    s.get_search(query)
    r = Result(s)

5) Agora como ler e salvar o resultado:
    # Para ver a quantidade de resultados
        print(r.manipulated["data"]["search"]["repositoryCount"])
    # Para ordenar o resutado por estrelas
        r.sortByStars()
    # Para salvar apenas os primeiros
        r.sliceFirsts(n)
    # Para salvar o resultado em .json
        r.toJson(filePath)
    # Para salvar o resultado em .xlsx
        r.toExcel(filePath)
"""

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



