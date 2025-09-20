import argparse
import requests
from github import Github

def fetch_pr_patch(token, repo_name, pr_number):
    # Authenticate with GitHub
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Get the PR object
    pr = repo.get_pull(pr_number)

    # Fetch patch using patch_url
    patch_url = pr.patch_url
    response = requests.get(patch_url)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch patch. Status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="GitHub PR Review Fetcher")
    parser.add_argument("--server", required=True, help="Server type, e.g., github")
    parser.add_argument("--repo", required=True, help="Repository in owner/repo format")
    parser.add_argument("--pr", type=int, required=True, help="Pull Request number")
    parser.add_argument("--token", required=False, help="GitHub Personal Access Token (optional, env preferred)")

    args = parser.parse_args()

    # Use token from argument or environment variable
    import os
    github_token = args.token or os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise Exception("GitHub token is required! Set it with --token or GITHUB_TOKEN environment variable.")

    print(f"=======================================================================")
    print(f"| Starting PR Review for {args.server}:{args.repo} PR #{args.pr} |")
    print(f"=======================================================================")

    try:
        patch_text = fetch_pr_patch(github_token, args.repo, args.pr)
        print(" PR Patch fetched successfully!\n")
        print(patch_text[:1000] + "\n...")  # print only first 1000 chars
    except Exception as e:
        print(f" Failed to fetch PR: {e}")

if __name__ == "__main__":
    main()
