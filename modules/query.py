

class Query():
    """
    Objeto que gera e armazena a query baseada nos parâmentros de entrada
    """

    def __init__(self,  keywords = {"include":[], "exclude":[]},
                        parameters = {"include":{}, "exclude":{}},
                        pag_count = 100, 
                        all_pages = False, 
                        more_filters = "",
                        others = {}):

        self.keywords = keywords
        self.parameters = parameters
        self.all_pages = all_pages
        self.string = more_filters
        self.pag_count = 100 if all_pages else pag_count
        self.others = others

        self.metadata = self.getMetadata()


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
        """
        Função necesaria para percorrer todas as páginas
        """
        self.others["after"] = str(last_index)


    def getMetadata(self):
        dic = {
            "keywords-include": ", ".join(self.keywords["include"]),
            "keywords-exclude": ", ".join(self.keywords["exclude"]),
            "parameters-include": ", ".join([f"{x}:{self.parameters['include'][x]}" for x in self.parameters['include']]),
            "parameters-exclude": ", ".join([f"{x}:{self.parameters['exclude'][x]}" for x in self.parameters['exclude']]),
            "Total": None, 
            "Utilizados": None, 
            "Data": None, 
            "Criterio de separacao": None,
        }
        return dic

    
    def returnMetadata(self):
        return self.metadata

    
    def getInterfaceInfo(self):
        dic = {
            "keywords-include": ", ".join(self.keywords["include"]),
            "keywords-exclude": ", ".join(self.keywords["exclude"]),
            "parameters-include": ", ".join([f"{x}:{self.parameters['include'][x]}" for x in self.parameters['include']]),
            "parameters-exclude": ", ".join([f"{x}:{self.parameters['exclude'][x]}" for x in self.parameters['exclude']]),
            "pag-count": self.pag_count,
            "all-pages": self.all_pages,
            "more-filters": self.string,
            "others": ", ".join([f"{x}:{self.others[x]}" for x in self.others]),
        }

        return dic
    
    
    def toCache(self):
        dic = {
            "keywords": self.keywords,
            "parameters": self.parameters,
            "pag_count": self.pag_count, 
            "all_pages": self.all_pages, 
            "more_filters": self.string,
            "others": self.others
        }
        return dic
