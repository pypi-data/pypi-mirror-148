import requests
from bs4 import BeautifulSoup
from random import choice
from sys import exit, argv
from webbrowser import open_new_tab
import webbrowser
from pprint import pprint


class nyaa:

    def __init__ (self, terms):
        self.search = terms
        self.url = None
        self.base = "https://nyaa.si/?f=0&c=1_2&q="
        self.itup = ()
        self.bestCand = None


    def get_itup(self):
        """returns the tuple of dicts of entry title, magnet url, seeds, and leeches. 
        Will receive an empty tuple if executed before nyaadata or main"""
        
        return self.itup 

    def get_search(self):
        """
        Returns the search terms used.
        """
        return self.search 

    def get_base(self):
        return self.base 

    def get_bestCand(self):
        """
        tuple with the best search candidate based on number of seeders. 
        """
        return self.bestCand

    def get_url(self):
        """
        returns the complete search URL. Use after URL make or the return value will be None.
        """
        return url

    def verify(self) -> bool:
        return isinstance(self.search, str)


    def rand_user_agent(self):
        ual = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        ]

        user_agent = choice(ual)
        return {"User-Agent": user_agent}

    def url_make(self):
        search = None
        if " " in self.search:
            sSplit = self.search.split(" ")
            search = "+".join(sSplit)
        else:
            search = self.search

        self.url = self.base + search

    def get_data(self):
        header = self.rand_user_agent()
        try:
            response = requests.get(self.url, headers = header)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"nyaa: Getting Search Data.... Resp. Code: {response.status_code}")
                #pprint(response.text)
                return response.text
            else:
                print(f"nyaa: The server threw code {reponse.status_code}. This does not allow access to http response.")
                exit(1)

        except Exception as ex: #clear up with more specific data
            print(f"nyaa: An error has occured: {ex}")
            exit(3) 

    def sort_data(self, resp):

        try:
            print("nyaa: sort_data: Starting....")
            soup = BeautifulSoup(resp, "html.parser")
            tr = soup.find_all("tr")
            
            

            for i in tr:
                info_dict = {
                    "Title": "",
                    "Magnet": "",
                    "Size": 0,
                    "Seed": 0,
                    "Leech": 0,
                }
                td = i.find_all("td")
                for e, d in enumerate(td):
                
                    if e == 1:
                        ahref = d.find_all("a")

                        for en, a in enumerate(ahref):
                            
                            if en == 0: #issue with title sorting.
                                
                                if not a.text.startswith("\n"):
                                    
                                    info_dict["Title"] = a.text
                                    break
                                
                            if en == 1:

                                info_dict["Title"] = a.text
                                

                    if e == 2:
                        mag = d.find_all("a")

                        for enu, m in enumerate(mag):
                            if enu == 1:
                                
                                info_dict["Magnet"] = m.get("href") # magnet

                    if e == 3:
                        info_dict["Size"] = d.text # size

                    if e == 5:
                        info_dict["Seed"] = int(d.text) # seeds

                    if e == 6:
                        info_dict["Leech"] = int(d.text) # leeches 

                        self.itup += (info_dict,)

                # pprint(self.itup)

        except Exception as ex:
            print("nyaa: sort_data:" +str(ex)) 

    def RepresentsInt(self):
        try: 
            int(self.search)
            return False
        except ValueError:
            return True

    def find_highest(self):


        try:
            highest = 0
            hi_d = None

            for f in self.itup:
                seeds = f["Seed"]
                leech = f["Leech"]
                if seeds > highest and leech < seeds:
                    highest = seeds
                    hi_d = f

            self.bestCand = hi_d
            print("nyaa: Best Candidate: {}".format(hi_d["Title"]))
        except TypeError as te:
            print("nyaa: No content available for your search.")
            exit(8)

    def browser_magnet(self):
        '''
        Pulls up magnetlink  in web browser tab.
        :return:
        '''
        try:
            magnet = self.bestCand["Magnet"]
            webbrowser.open(magnet, new = 0, autoraise = true)
        except Exception as ex:
            print("nyaa: Terms were not matched completely or at all. Try again with different terms.")
            exit(7)

    def nyaadata(self):

        data = None
        if self.verify():
            self.url_make()
            data = self.get_data()
            self.sort_data(data)

    def main(self):

        data = None
        if self.verify():
            self.url_make()
            data = self.get_data()
            self.sort_data(data)
            self.find_highest()
            self.browser_magnet()
        else:
            print("nyaa: the search terms were not string type data.")
       
def argcontrol():
    arglen = len(argv)
    search = None
    if arglen == 2:
        print(f"nyaa: Fetching the best magnet link for search terms {argv[1]}.")
        search = argv[1]
    else:
        search = input("nyaa: Enter Search Terms:")
    
    n = nyaa(search)
    n.main()

if __name__ == "__main__":

    argcontrol()

    