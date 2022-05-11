from webbrowser import get
import requests
import json
import os
import pandas as pd


ACCESS_TOKEN = ""

with open("C:\Code\git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()


def token_auth(request):
    request.headers["User-Agent"] = "wobetec" # Necessário
    request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
    return request


class Query_string():
    """
    Objeto construido a partir de um dicionário e que ao usar __str__() retorna a string da query para realizar o request

    Argumentos aceitos no dicionário:
        --> keywords = dicionário contendo duas listas de termos "include" e "exclude"
        --> parameters = dicionário contendo dois dicionários com os parametros a serem adcionas ou excluidos
        --> pag_count = quantidade de resultados esperados no retorno da request 
    """

    def __init__(self,  keywords = {"include":[], "exclude":[]},
                        parameters = {"include":{}, "exclude":{}},
                        pag_count = 100, 
                        all_pages = False, 
                        more_filters = ""):
        

        self.keywords = keywords
        self.parameters = parameters
        self.all_pages = all_pages
        self.string = more_filters
        self.pag_count = 100 if all_pages else pag_count
        self.others = {}


    def __str__(self):
        key_in = [f"""\\"{x}\\" """ for x in self.keywords["include"]]
        key_ex = [f"""NOT \\"{x}\\" """ for x in self.keywords["exclude"]]
        str_keywords = " ".join(key_in) + "" + " ".join(key_ex)

        par_in = [f"""{x}:\\"{self.parameters["include"][x]}\\" """ for x in self.parameters["include"]]
        par_ex = [f"""NOT {x}:\\"{self.parameters["exclude"][x]}\\" """ for x in self.parameters["exclude"]]
        str_parameters = " ".join(par_in) + " " + " ".join(par_ex)

        
        others = ""
        others += ", type: REPOSITORY"
        others += ", first: " + str(self.pag_count)

        for key in self.others:
            others += """, {}:\"{}\" """.format(key, self.others[key])


        main = f"\"{str_keywords} {str_parameters}\" {others}"

        query = """{
            search(query: """ + main +"""  ) {
                repositoryCount
                pageInfo {
                    startCursor
                    hasPreviousPage
                    hasNextPage
                    endCursor
                }
                nodes {
                    ... on Repository {
                            name
                            url
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
            }"""

        return query
    

    def change_last_index(self, last_index):
        self.others["after"] = str(last_index)


class Search():
    """
    Classe que gera o buscador responsável por fazer as queries
    """

    global SITE 
    global ACCESS_TOKEN

    SITE = "https://api.github.com/graphql"


    def __init__(self):
        self.response = None
        self.in_cache = False
        pass    


    def get_search(self, query):
        """
        Função que realiza a busca, inclusive buscas em sequência(all_pages)
        """
        
        string = str(query)
        
        if string != "":
            response = requests.post(SITE, json = {"query":string}, auth=token_auth)
        else:
            response = requests.get(SITE, auth=ACCESS_TOKEN)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            self.response = None
        else:

            self.response = response.json()

            if self.response["data"]["search"]["pageInfo"]["hasNextPage"] and query.all_pages:
                last = self.response["data"]["search"]["pageInfo"]["endCursor"]
                self.get_all_pages(query, last)

            self.to_file()
            self.in_cache = True

    
    def get_all_pages(self, query, last):
        query.change_last_index(last)

        string = str(query)
        

        response = requests.post(SITE, json = {"query":string}, auth=token_auth)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
        else:
            response = response.json()
            
            self.response["data"]["search"]["nodes"].extend(response["data"]["search"]["nodes"])
        

            if response["data"]["search"]["pageInfo"]["hasNextPage"]:
                last = response["data"]["search"]["pageInfo"]["endCursor"]
                self.get_all_pages(query, last)


    def sort_repos_stars(self):
        nodes = self.response["data"]["search"]["nodes"]
        new_list = sorted(nodes, key=lambda node: node["stargazers"]["totalCount"], reverse=True)
        self.response["data"]["search"]["nodes"] = new_list
        self.to_file()


    def get_firsts(self, n):
        nodes = self.response["data"]["search"]["nodes"]
        self.response["data"]["search"]["nodes"] = nodes[:n]
        self.to_file()


    def results(self):
        with open("temp/result.json", "r") as f:
            file = json.load(f)
        json_formated = json.dumps(file, indent=4)
        print(json_formated)


    def to_file(self):
        with open("temp/result.json", "w") as f:
            f.write(json.dumps(self.response, indent=4))


    def to_excel(self):
        with open("temp/result.json", "r") as f:
            file = json.load(f)

        dic = file["data"]["search"]["nodes"]

        lista = [[item["name"], item["url"], item["stargazers"]["totalCount"]] for item in dic]

        df = pd.DataFrame(lista, columns=["name", "url", "star"])

        df.to_excel("result.xlsx", index=False)



    def __str__(self):
        if self.in_cache:
            with open("temp/result.self", "r") as f:
                file = json.load(f)
            json_formated = json.dumps(self.response, indent=4)
            return json_formated
        else:
            return "Not in cache."
        pass


if __name__ == "__main__":
    s = Search()

    keywords = {"include":["paper", "experiments"], "exclude":["machine learning", "neural network", "artificial intelligence", "framework", "train"]}
    parameters = {"include":{"language":"python"}, "exclude":{}}

    query = Query_string(keywords, parameters, pag_count=100, all_pages = True)
    s.get_search(query)

    try:
        print(s.response["data"]["search"]["repositoryCount"])
    except:
        pass
    pass

    s.sort_repos_stars() #ordena a busca por stars
    s.get_firsts(100) #pega apenas os n primieros da busca
    s.to_excel() #salva a busca em um .xlsx

