import requests
import json
import urllib
import filetype
import os
import re
import git
import shutil

from termcolor import cprint 
from pathlib import Path
from os import path


print("Username : ")
user = input()
if path.exists(f"./{user}/github"):
	shutil.rmtree(f"./{user}/github")
else:
	Path(f"./{user}/github").mkdir(parents=True, exist_ok=True)

API_URL = "https://api.instantusername.com"

main_service_page = requests.get(f'https://api.instantusername.com/services') 
data = main_service_page.json()

endpoint = data[8]['endpoint'] 

api_user_url = API_URL + endpoint  
api_user_url = api_user_url.replace("{username}", user) 
api_user_page = requests.get(api_user_url) 
user_data = api_user_page.json() 

if user_data['available'] == False: 
	user_url = user_data.get('url')
	cprint(f"GitHub URL of {user} is {user_url}", 'cyan'),
else:
	cprint(f"No user exists by the username {user}", 'red')

github_user_api = requests.get(f"https://api.github.com/users/{user}")
github_user_data = github_user_api.json()

def image():
	
	Path(f"./{user}/github").mkdir(parents=True, exist_ok=True)	
	user_avatar_url = str(github_user_data.get('avatar_url'))
	urllib.request.urlretrieve(user_avatar_url, f"./{user}/github/profile_pic")
	kind = filetype.guess(f"./{user}/github/profile_pic")
	os.rename(rf'./{user}/github/profile_pic', rf'./{user}/github/profile_pic.{kind.extension}')

def user_follow():
		
	page_num = 1
	follower_url = github_user_data['followers_url']
	follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
	follower_data = follower_api_page.json()

	number_of_follower = github_user_data['followers']
	cprint(f'Number of Followers are : {number_of_follower}', 'green')

	remaining_follower = number_of_follower % 100
	num_of_pages = number_of_follower / 100 

	def num():
		i = 0
		for i in range(0, 100):

			followers = follower_data[i].get('login')

			file = open(f"./{user}/github/followers.txt", 'a')
			file.write(followers + "\n")
			file.close()
			i = i + 1

	while page_num <= num_of_pages:
		follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
		follower_data = follower_api_page.json()
		num()
		page_num = page_num + 1
		

	follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
	follower_data = follower_api_page.json()	
	i = 0
	for i in range(0, int(remaining_follower)):

		followers = follower_data[i].get('login')

		file = open(f"./{user}/github/followers.txt", 'a')
		file.write(followers + "\n")
		file.close()
		i = i + 1

def user_following():
	page_num = 1
	following_url = github_user_data['followers_url']
	following_api_page = requests.get(following_url+f'?per_page=100&page={page_num}')
	following_data = following_api_page.json()

	number_of_following = github_user_data['following']
	cprint(f"Number of Following are : {number_of_following}\n", 'green')

	remaining_following = number_of_following % 100
	num_of_pages = number_of_following / 100 

	def num():
		i = 0
		for i in range(0, 100):

			following = following_data[i].get('login')

			file = open(f"./{user}/github/following.txt", 'a')
			file.write(following + "\n")
			file.close()
			i = i + 1
		
	while page_num <= num_of_pages:
		follower_api_page = requests.get(follower_url+f'?per_page=100&page={page_num}')
		follower_data = follower_api_page.json()
		num()
		page_num = page_num + 1

	following_api_page = requests.get(following_url+f'?per_page=100&page={page_num}')
	following_data = following_api_page.json()	
	i = 0
	for i in range(0, int(remaining_following)):
		following = following_data[i].get('login')

		file = open(f"./{user}/github/following.txt", 'a')
		file.write(following + "\n")
		file.close()
		i = i + 1

def info():

	user_name = github_user_data.get('name')
	company = github_user_data.get('company')
	blog= github_user_data.get('blog')
	location = github_user_data.get('location')
	email = github_user_data.get('email')
	bio = github_user_data.get('bio')
	twitter_username = github_user_data.get('twitter_username')

	file = open(f"./{user}/github/info.txt", 'a')

	if user_name and user_name.strip():
		file.write(f"Name of the user {user} is {user_name}\n")
		cprint(f"Name of the {user} is {user_name}", 'yellow')

	if company and company.strip():
		file.write(f"Company at which {user} works at is {company}\n")
		cprint(f"Company at which {user} works at is {company}", 'yellow')

	if blog and blog.strip():
		file.write(f"{user} has blog at {blog}\n")
		cprint(f"{user} has blog at {blog}", 'yellow')

	if location and location.strip():
		file.write(f"{user} lives at {location}\n")
		cprint(f"{user} lives at {location}", 'yellow')

	if email and email.strip():
		file.write(f"{user}'s email is {email}")
		cprint(f"{user}'s email is {email}", 'yellow')

	if bio and bio.strip():
		file.write(f"{user}'s bio is {bio}\n")
		cprint(f"{user}'s bio is {bio}", 'yellow')

	if twitter_username and twitter_username.strip():
		file.write(f"{user}'s Twitter Username is {twitter_username}\n")
		cprint(f"{user}'s Twitter profile is https://twitter.com/{twitter_username}\n", 'yellow')

	file.close()	

def repo():
	page_num = 1
	repos_url = github_user_data['repos_url']
	repos_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
	repos_data = repos_api_page.json()

	number_of_repos = github_user_data['public_repos']
	cprint(f"Number of Public repos of {user} are {number_of_repos}\n")


	remaining_repos = number_of_repos % 100
	num_of_pages = number_of_repos / 100

	def num():
		i = 0
		for i in range(0, 100):
			repos = repos_data[i].get('html_url')

			file = open(f"./{user}/github/repos.txt", 'a')
			file.write(repos + "\n")
			file.close()
				
			i = i + 1

	while page_num <= num_of_pages:
		repo_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
		repos_data = repo_api_page.json()
		num()
		page_num = page_num + 1

	repos_api_page = requests.get(repos_url+f'?per_page=100&page={page_num}')
	repos_data = repos_api_page.json()
	i = 0
	for i in range(0, int(remaining_repos)):
		repos = repos_data[i].get('html_url')

		file = open(f"./{user}/github/repos.txt", 'a')
		file.write(repos + "\n")
		file.close()

		i = i + 1

def clonerepo():

	Path(f"./{user}/github/repos").mkdir(parents=True, exist_ok=True)
	cprint("Do you want to clone all the repos locally (y/n): \n", 'blue')
	answer = input()

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

def github():
	image()
	user_follow()
	user_following()
	info()
	repo()
	clonerepo()

	
