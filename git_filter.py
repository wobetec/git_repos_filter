from webbrowser import get
import requests
import json
import os

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
        



class Search():

    global SITE 
    global ACCESS_TOKEN

    SITE = "https://api.github.com/graphql"

    def __init__(self):
        pass


    def get_query(self, keywords = [], parameters = {}):
        string = " ".join(keywords)
        for key in parameters:
            string += " {}:{}".format(key, parameters[key])
        
        if string != "":
            query = """{
                search(query: \"""" + f"{string}" + """\", type: REPOSITORY, first: 1, after: \"Y3Vyc29yOjE=\") {
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
        else:
            return ""


    def get_search(self, keywords = [], parameters = {}):
        query = self.get_query(keywords, parameters)
        if query != "":
            response = requests.post(SITE, json = {"query":query}, auth=token_auth)
        else:
            response = requests.get(SITE, auth=ACCESS_TOKEN)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            return None
        else:
            return response


    def results(self, response):
        json_formated = json.dumps(response.json(), indent=4)
        print(json_formated)


    def to_file(self, response, file_name):
        with open(file_name, "w") as f:
            f.write(self.results(response))


if __name__ == "__main__":
    s = Search()

    keywords = ["paper", "experiments"]
    parameters = {"language":"python"}

    response = s.get_search(keywords, parameters)
    s.results(response)

    #s.to_file(response, "query2.txt")

    pass

