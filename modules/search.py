from datetime import date
import requests
import json
from datetime import datetime


#Seção de acesso à API
ACCESS_TOKEN = ""

with open("modules/token/git_token.txt", "r") as f:
    ACCESS_TOKEN = f.read()


def token_auth(request):
    request.headers["User-Agent"] = "wobetec"
    request.headers["Authorization"] = "token {}".format(ACCESS_TOKEN)
    return request


class Search():
    """
    Buscador que recebe query e retornar results
    """

    global SITE 
    global ACCESS_TOKEN

    SITE = "https://api.github.com/graphql"


    def __init__(self):
        self.response = None
        self.time = None
        self.metadata = None


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
            self.response = None
        else:
            
            self.response = response.json()

            if self.response["data"]["search"]["pageInfo"]["hasNextPage"] and query.all_pages:
                last = self.response["data"]["search"]["pageInfo"]["endCursor"]
                self.get_all_pages(query, last)

        
        self.time = datetime.now()

        self.metadata = query.returnMetadata()

        self.metadata["Total"] = self.response["data"]["search"]["repositoryCount"]
        self.metadata["Data"] = self.time.strftime("%d/%m/%Y")

        return  response.status_code

    
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

