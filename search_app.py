import requests
import json

class Search():

    global SITE 
    global ACCESS_TOKEN

    SITE = "http://localhost:5000/"
    ACCESS_TOKEN = ""

    def __init__(self):
        with open("git_token.txt", "r") as f:
            ACCESS_TOKEN = f.read()

    def token_auth(request):
        request.headers["User-Agent"] = "Minicurso" # Necessário
        request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
        return request

    def get_query(self, keywords = [], parameters = {}):
        
        string = " ".join(keywords)
        for key in parameters:
            string += " {}:{}".format(key, parameters[key])
        
        if string != "":
            query = """{
                search(query: \"""" + f"{string}" + """\", type: REPOSITORY, first: 10) {
                    repositoryCount
                    nodes {
                        ... on Repository {
                            name
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
            response = requests.post(SITE, json = {"query":query}, auth=Search.token_auth)
        else:
            response = requests.get(SITE, auth=ACCESS_TOKEN)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
        else:
            return response.json()

    def results(self, response):
        json_formated = json.dumps(response.json())
        return json_formated

if __name__ == "__main__":
    s = Search()
    response = s.get_search(keywords = ["python"], parameters = {"language":"python"})
    print(s.results(response))
    pass

