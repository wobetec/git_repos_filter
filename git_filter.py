from webbrowser import get
import requests
import json
import os
import pandas as pd


ACCESS_TOKEN = ""

with open("C:\Code\git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()

def token_auth(request):
    request.headers["User-Agent"] = "Minicurso" # Necessário
    request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
    return request

class Query_string():

    def __init__(self, keywords = [], parameters = {}, pag_count = 100, all_pages = False, more = {}):
        self.keywords = keywords
        self.parameters = parameters
        self.all_pages = all_pages
        self.others = more
        self.pag_count = 100 if all_pages else pag_count


    def __str__(self):
        str_keywords = " ".join(self.keywords)
        str_parameters = ""
        for key in self.parameters:
            str_parameters += """ {}:\\"{}\\" """.format(key, self.parameters[key])

        #search string
        string = f"{str_keywords} {str_parameters}"
        others = ""
        others += ", type: REPOSITORY"
        others += ", first: " + str(self.pag_count)

        for key in self.others:
            others += """, {}:\"{}\" """.format(key, self.others[key])

        query = """{
            search(query: \"""" + string + """\" """ + others + """ ) {
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

    global SITE 
    global ACCESS_TOKEN

    SITE = "https://api.github.com/graphql"


    def __init__(self):
        self.response = None
        self.in_cache = False
        pass    


    def get_search(self, query):
        
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


    def results(self):
        json_formated = json.dumps(self.response, indent=4)
        print(json_formated)


    def to_file(self):
        with open("temp/result.txt", "w") as f:
            f.write(json.dumps(self.response, indent=4))


    def to_excel(self):
        with open("temp/result.txt", "r") as f:
            file = json.load(f)

        dic = file["data"]["search"]["nodes"]

        lista = [[item["name"], item["url"]] for item in dic]

        df = pd.DataFrame(lista, columns=["name", "url"])

        df.to_excel("result.xlsx", index=False)



    def __str__(self):
        if self.in_cache:
            with open("temp/result.txt", "r") as f:
                file = json.load(f)
            json_formated = json.dumps(self.response, indent=4)
            return json_formated
        else:
            return "Not in cache."
        pass


if __name__ == "__main__":
    s = Search()

    keywords = ["paper", "experiments"]
    parameters = {"language":"python"}

    query = Query_string(keywords, parameters, pag_count=100, all_pages = True)

    s.get_search(query)
    s.sort_repos_stars()
    #print(str(s))

    pass

