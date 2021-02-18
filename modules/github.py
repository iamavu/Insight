#Github

import requests
import json
import urllib
import filetype
import os
import re
import git
import shutil

from .username import *
from os import path
from termcolor import cprint 
from pathlib import Path

def github():

    
    user = userFetcher.getUser()
    api_url = "https://api.github.com/users/" + user
    api_page = requests.get(api_url)
    user_data = api_page.json()
    user_url = user_data.get('html_url')

    def checkAPI():
        apiLimit_page = requests.get("https://api.github.com/rate_limit")

        apiData = apiLimit_page.json()
        data = apiData['resources']['core']['remaining']
        if data < 10:
            cprint("API Limt Exceeded for your IP, please try again after a while", 'red')
            global exceeded
            exceeded = True
        else:
            exceeded = False
            pass

    def user_check():

        if user_data.get('message') == 'Not Found':
            cprint(f"User {user} not found", 'red')
            global userExist
            userExist = False
            
        else:
            userExist = True
            
    def userURL():
        cprint(f"GitHub URL of {user} is {user_url}\n", 'cyan')
    
    def folder():

        if path.exists(f"./{user}/github"):
            shutil.rmtree(f"./{user}/github")
        else:
            pass

    def image():

        Path(f"./{user}/github").mkdir(parents=True, exist_ok=True)	
        user_avatar_url = str(user_data.get('avatar_url'))
        urllib.request.urlretrieve(user_avatar_url, f"./{user}/github/profile_pic")
        kind = filetype.guess(f"./{user}/github/profile_pic")
        os.rename(rf'./{user}/github/profile_pic', rf'./{user}/github/profile_pic.{kind.extension}')

    def user_follow():

        page_num = 1
        follower_url = user_data['followers_url']
        follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
        follower_data = follower_api_page.json()

        number_of_follower = user_data['followers']
        cprint(f'Number of Followers are : {number_of_follower}', 'green')

        remaining_follower = number_of_follower % 100
        num_of_pages = (number_of_follower / 100)

        def num():

            for i in range(0, 100):

                followers = follower_data[i].get('login')

                file = open(f"./{user}/github/followers.txt", 'a')
                file.write(followers + "\n")
                file.close()
        
        while page_num <= num_of_pages:
            follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
            follower_data = follower_api_page.json()
            num()
            page_num = page_num + 1
        
        follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
        follower_data = follower_api_page.json()	

        for i in range(0, int(remaining_follower)):

            followers = follower_data[i].get('login')

            file = open(f"./{user}/github/followers.txt", 'a')
            file.write(followers + "\n")
            file.close()

        

    def user_following():

        page_num = 1
        following_url = user_data['following_url']
        following_url = following_url.replace('{/other_user}', '')
        following_api_page = requests.get(following_url+f'?per_page=100&page={page_num}')
        following_data = following_api_page.json()

        number_of_following = user_data['following']
        cprint(f"Number of Following are : {number_of_following}\n", 'green')

        remaining_following = number_of_following % 100
        num_of_pages = (number_of_following / 100) 

        def num():

            for i in range(0, 100):

                following = following_data[i].get('login')

                file = open(f"./{user}/github/following.txt", 'a')
                file.write(following + "\n")
                file.close()
        
        while page_num <= num_of_pages:
            follower_api_page = requests.get(following_url+f'?per_page=100&page={page_num}')
            follower_data = follower_api_page.json()
            num()
            page_num = page_num + 1
        
        follower_api_page = requests.get(following_url+f'?per_page=100&page={page_num}')
        follower_data = follower_api_page.json()	

        for i in range(0, int(remaining_following)):

            followers = follower_data[i].get('login')

            file = open(f"./{user}/github/following.txt", 'a')
            file.write(followers + "\n")
            file.close()
 



    def info():

        user_name = user_data.get('name')
        company = user_data.get('company')
        blog= user_data.get('blog')
        location = user_data.get('location')
        email = user_data.get('email')
        bio = user_data.get('bio')
        twitter_username = user_data.get('twitter_username')

        file = open(f"./{user}/github/info.txt", 'a')

        if user_name and user_name.strip():
            file.write(f"Possibl real name of the user {user} is {user_name}\n")
            cprint(f"Possible real name of the {user} is {user_name}", 'green')

        if company and company.strip():
            file.write(f"Company at which {user} works at is {company}\n")
            cprint(f"Company at which {user} works at is {company}", 'green')

        if blog and blog.strip():
            file.write(f"{user} has blog at {blog}\n")
            cprint(f"{user} has blog at {blog}", 'green')

        if location and location.strip():
            file.write(f"{user} lives at {location}\n")
            cprint(f"{user} lives at {location}", 'green')

        if email and email.strip():
            file.write(f"{user}'s email is {email}")
            cprint(f"{user}'s email is {email}", 'green')

        if bio and bio.strip():
            file.write(f"{user}'s bio is {bio}\n")
            cprint(f"{user}'s bio is {bio}", 'green')

        if twitter_username and twitter_username.strip():
            file.write(f"{user}'s Twitter Username is {twitter_username}\n")
            cprint(f"{user}'s Twitter profile is https://twitter.com/{twitter_username}\n", 'green')

        file.close()       



    def repo():
        page_num = 1
        repos_url = user_data['repos_url']
        repos_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
        repos_data = repos_api_page.json()

        number_of_repos = user_data['public_repos']
        cprint(f"Number of Public repos of {user} are {number_of_repos}\n", 'green')


        remaining_repos = number_of_repos % 100
        num_of_pages = number_of_repos / 100

        def num():
            
            for i in range(0, 100):
                repos = repos_data[i].get('html_url')

                file = open(f"./{user}/github/repos.txt", 'a')
                file.write(repos + "\n")
                file.close()

        while page_num <= num_of_pages:
            repo_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
            repos_data = repo_api_page.json()
            num()
            page_num = page_num + 1

        repos_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
        repos_data = repos_api_page.json()

        for i in range(0, int(remaining_repos)):
            repos = repos_data[i].get('html_url')

            file = open(f"./{user}/github/repos.txt", 'a')
            file.write(repos + "\n")
            file.close()    

    def clonerepo():

        Path(f"./{user}/github/repos").mkdir(parents=True, exist_ok=True)
        answer = input("Do you want to clone all the repos locally (y/n): ")

        if answer == 'y':
            cprint("Cloning the repos...", 'white')
            with open(f'./{user}/github/repos.txt') as file:
                for line in file:
                    urls = re.findall('https?://\S+',line)
                    git.Git(f"./{user}/github/repos").clone(urls[0])

                        

        elif answer == 'n' :
            cprint(f"Not cloning the repos", 'red')
        else:
            cprint(f"Wrong Choice", 'red')
            clonerepo()

    def folder_creation():
        cprint(f"GitHub folder of {user} has been created in the current directory", 'cyan')
    
    checkAPI()
    user_check()
    if exceeded == False and userExist == True:
            user_url()
            folder()
            image()
            user_follow()
            user_following()
            info()
            repo()
            clonerepo()
            folder_creation()

    else:
        pass


if __name__ == '__main__':
    
    github()

        

