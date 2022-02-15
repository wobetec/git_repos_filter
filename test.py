import requests
import json

SITE = "http://localhost:5000/"
ACCESS_TOKEN = ""

with open("git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()

def token_auth(request):
    request.headers["User-Agent"] = "wobetec" # Necessário
    request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
    return request

def get_query(keywords = [], parameters = {}):
        
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

query = get_query(keywords = ["python"], parameters={"language":"python"})

response = requests.post(SITE, json = {"query":query}, auth=token_auth)

def results(response):
    json_formated = json.dumps(response.json())
    return json_formated

print(response.status_code)
print(results(response))