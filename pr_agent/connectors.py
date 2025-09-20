# pr_agent/connectors.py
import os
from abc import ABC, abstractmethod
from github import Github, Auth

class GitClient(ABC):
    """Abstract base class for all git server clients."""

    @abstractmethod
    def fetch_pr_details(self, repo_name: str, pr_number: int):
        pass

    @abstractmethod
    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        pass

class GitHubClient(GitClient):
    """GitHub client using PyGithub."""

    def __init__(self, token: str):
        if not token:
            raise ValueError("GitHub token is not set. Please set GITHUB_TOKEN environment variable.")
        self.github = Github(auth=Auth.Token(token))

    def _get_repo(self, repo_name):
        return self.github.get_repo(repo_name)

    def _get_pr(self, repo_name, pr_number):
        repo = self._get_repo(repo_name)
        return repo.get_pull(pr_number)

    def fetch_pr_details(self, repo_name: str, pr_number: int):
        try:
            pr = self._get_pr(repo_name, pr_number)
            return pr
        except Exception as e:
            print(f"Error fetching PR #{pr_number} details: {e}")
            return None

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        try:
            pr = self._get_pr(repo_name, pr_number)
            return pr.get_patch()
        except Exception as e:
            raise e

def get_git_client(server_type: str):
    """Factory to return Git client instance."""
    server_type = server_type.lower()
    if server_type == "github":
        token = os.getenv("GITHUB_TOKEN")
        return GitHubClient(token)
    else:
        raise NotImplementedError(f"{server_type} client not implemented yet.")
