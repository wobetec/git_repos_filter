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

    def __init__(self, keywords = [], parameters = {}, pag_count = 100):
        self.keywords = keywords
        self.parameters = parameters
        self.pag_count = pag_count


    def __str__(self):
        str_keywords = " ".join(self.keywords)
        str_parameters = ""
        for key in self.parameters:
            str_parameters += " {}:{}".format(key, self.parameters[key])

        #search string
        string = f"{str_keywords} {str_parameters}"
        others = ""
        others += ", type: REPOSITORY"
        others += ",first: " + str(self.pag_count)

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
                    }
                }
            }
        }"""

        return query
        

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
            self.to_file()
            self.in_cache = True
            


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

    keywords = ["scientific", "experiments"]
    parameters = {"language":"python"}

    query = Query_string(keywords, parameters)

    s.get_search(query)
    print(str(s))

    pass

