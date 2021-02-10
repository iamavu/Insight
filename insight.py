#!/usr/bin/env python
#INSIGHT - The OSINT Tool

__version__ = '0.0.1'

from modules.github import *
from termcolor import cprint

def banner():
	cprint("""


  _____           _       _     _   
  \_   \_ __  ___(_) __ _| |__ | |_ 
   / /\/ '_ \/ __| |/ _` | '_ \| __|
/\/ /_ | | | \__ \ | (_| | | | | |_ 
\____/ |_| |_|___/_|\__, |_| |_|\__|
                    |___/           
				> OSINT Tool
				> Created by iamavu


                    """, 'magenta')



if __name__ == '__main__':

	banner()
	github()
	cprint(f"Folder of user {user} has been created in the current directory!", 'blue')



