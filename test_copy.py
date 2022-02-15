import requests
import json

SITE = "https://api.github.com/graphql" #"http://localhost:5000/"
ACCESS_TOKEN = ""

with open("C:\Code\git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()
    print(ACCESS_TOKEN)

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
                search(query: \"""" + f"{string}" + """\", type: REPOSITORY, first: 100) {
                    repositoryCount
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

query = get_query(keywords = ["scientific", "experiment"], parameters={"language":"python"})

response = requests.post(SITE, json = {"query":query}, auth=token_auth)

def results(response):
    json_formated = json.dumps(response.json())
    return json_formated

print(response.status_code)
print(results(response))
with open("result.txt", "w") as f:
    f.write(results(response))