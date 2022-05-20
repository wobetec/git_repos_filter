import requests
import json

#Seção de acesso à API
ACCESS_TOKEN = ""

with open("C:\Code\git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()


def token_auth(request):
    request.headers["User-Agent"] = "wobetec"
    request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
    return request


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

        df.to_excel("./temp/result.xlsx", index=False)



    def __str__(self):
        if self.in_cache:
            with open("./temp/result.self", "r") as f:
                file = json.load(f)
            json_formated = json.dumps(self.response, indent=4)
            return json_formated
        else:
            return "Not in cache."
        pass
