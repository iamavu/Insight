#INSIGHT
version= '0.0.2'

from modules.username import *
from modules.github import *
from termcolor import cprint

def banner():
	cprint(f"""


  _____           _       _     _   
  \_   \_ __  ___(_) __ _| |__ | |_ 
   / /\/ '_ \/ __| |/ _` | '_ \| __|
/\/ /_ | | | \__ \ | (_| | | | | |_ 
\____/ |_| |_|___/_|\__, |_| |_|\__|
                    |___/           
				> OSINT Tool
				> Created by iamavu
                                > v{version}

                    """, 'magenta')

def insight():
    banner()
    userFetcher.setUser()
    github()
    

if __name__ == '__main__':
    insight()


    



