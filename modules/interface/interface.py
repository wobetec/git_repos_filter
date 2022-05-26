import os 
from pyfiglet import Figlet

from time import sleep

from modules.interface.inquirer import query

class GraphicsInterface():

    def __init__(self):
        pass

    
    def title(self, begin):
        self.clearScreen()
        f = Figlet(font='slant')
        print(f.renderText("Git Filter"))
        if begin:
            print("Wellcome to GitFilter! This tool is powred by wobetec.")
            sleep(3)
        else:
            print("See ya! Thanks for use us.")
            sleep(2)


    def queryShow(self, query):
        dic = query.getInterfaceInfo()
        print("Query = {")
        print(f"    keywords-include: {dic['keywords-include']}")
        print(f"    keywords-exclude: {dic['keywords-exclude']}")
        print(f"    parameters-include: {dic['parameters-include']}")
        print(f"    parameters-exclude: {dic['parameters-exclude']}")
        print(f"    pag-count: {dic['pag-count']}")
        print(f"    all-pages: {dic['all-pages']}")
        print(f"    more-filters: {dic['more-filters']}")
        print(f"    others: {dic['others']}") 
        print("}")


    def resultsShow(self, results):
        print("+----------+-----------+-----------+-----------+-----------+-----------+")
        print(f"|Results==>|{results[0].ljust(11)}|{results[1].ljust(11)}|{results[2].ljust(11)}|{results[3].ljust(11)}|{results[4].ljust(11)}|")
        print("+----------+-----------+-----------+-----------+-----------+-----------+")


    def commandLine(self, returned = ""):
        print("Terminal('>>>help' to get help):")
        print(f">>>{returned}")
        command = input(">>>")
        return command


    def clearScreen(self):
        if(os.name == 'posix'):# posix is os name for linux or mac
            os.system('clear')
        else:
            os.system('cls')




if __name__ == '__main__':
    pass