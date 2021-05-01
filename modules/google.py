#Google

from os import name
from urllib import parse
import requests
import re

from termcolor import cprint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urlparse
from urllib.parse import unquote
from .username import *
from .github import *


def google():
    ua = UserAgent()
    headers =   {
                'user-agent': ua.random
                }

    user = userFetcher.getUser()
    user = '"' + user + '"'
    page = requests.get("https://www.google.com/search?q={}&num=15".format(user), headers = headers )
    soup = BeautifulSoup(page.content, 'html.parser')
    google_search_results = []
    links = []

    def folder():
        if path.exists(f"./{user}/google"):
            shutil.rmtree(f"./{user}/google")
        else:
            pass
    Path(f"./{user}/google".replace('"', '')).mkdir(parents=True, exist_ok=True)

    def gather_links():
        cprint(f"Gathering links for {user}".replace('"', ''), "yellow")
        #find all the links from google search results
        try:
            for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
                google_search_results.append(re.split(":(?=http)",link["href"].replace("/url?q=","").split('&')[0]))
                if google_search_results != None:
                    pass
                else:
                    gather_links()
        except:
            cprint("Uh-oh Error Occured, Please run the script again", "red")
        data = google_search_results[:-2 or None]

        #decode URLs
        for link in data:
            link = "".join(link)
            link = unquote(link)
            links.append(link)
        
        for link in links:
            file = open(f"./{user}/google/links.txt".replace('"', ''), 'a')
            file.write(link + "\n")
            file.close()

        #check status code of URLs 
        cprint("Printing the URLs found with their response codes\n","yellow")
        for link in links:
            link = "".join(link)
            try:
                response = requests.get(link)
                cprint(f"Response Code for {link} is {response.status_code}",'cyan')
            except requests.exceptions.ConnectionError:
                cprint(f"{link} seems unreachable D:", "red")

    def dev():
        domains = []
        for link in links:
            link = "".join(link)
            parse = urlparse(link)
            domains.append(parse[1])
        
        #check if user has dev profiles
        dev = ['github', 'gitlab', 'stackexchange', 'devdocs', 'ycombinator', 'leetcode', 'hackerrank', 'sourceforge', 'bitbucket']
        isDev = False
        for dev_profile in dev:
            for domain in domains:
                if dev_profile in domain: 
                    isDev = True
                else:
                    pass
        if isDev == True:
            print('\n')
            cprint(f"{user} is probably into programming".replace('"',''), "green")
            cprint(f"Do you want to run the GitHub Module for the user?[y/n]","yellow")
            choice = input(">")
            print('\n')
            if choice == 'y' or choice == 'Y':
                github()
            else:
                cprint("Not runnning the GitHub Module", "yellow")
                print("\n")
        else:
            pass
        
    def real_name():
        linkedin_name = []
        name = user + " linkedin"
        search = requests.get("https://www.google.com/search?q={}&num=1".format(name), headers = headers )
        linkedin_soup = BeautifulSoup(search.content, 'html.parser')

        for link in linkedin_soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            linkedin_name.append(re.split(":(?=http)",link["href"].replace("/url?q=","").split('&')[0]))
            if linkedin_name == None and 'www.linkedin.com' in linkedin_name:
                cprint(f"LinkedIn for {user} doesn't exist")
            else:
                pass
        try:
            link_name = linkedin_soup.find('h3').text
            name = link_name.split()
            name = name[0] + ' ' + name[1]
            cprint(f"{user}'s possible real name is {name}(via LinkedIn)".replace('"',''),"green")
            file = open(f"./{user}/google/name.txt".replace('"', ''), 'a')
            file.write(f"{user}'s possible real name is {name}(via LinkedIn)".replace('"', ''))
            file.close()
        except AttributeError:
            print(f"{user} probably doesn't have LinkedIn")

    def folder_creation():
        cprint(f"Folder of {user} has been created in the current directory".replace('"', ''), 'cyan')
    
    folder()           
    gather_links()
    dev()
    real_name()
    folder_creation()
    

