from github import Github, Auth
import os

token = os.getenv("GITHUB_TOKEN")
g = Github(auth=Auth.Token(token))
