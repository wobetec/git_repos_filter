import pandas as pd
import json

with open("result.txt", "r") as f:
    file = json.load(f)

dic = file["data"]["search"]["nodes"]

lista = [[item["name"], item["url"]] for item in dic]

df = pd.DataFrame(lista, columns=["name", "url"])

df.to_excel("lista.xlsx", index=False)
