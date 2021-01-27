import os
import re
import json

from collections import defaultdict
from dotenv import load_dotenv

from github import Github
from github.GithubException import RateLimitExceededException


cases = {'Travis': '.travis.yml', 'GitHub': '.github'}
results_path = './ci_files/'


def authenticate(access_token):
    """
    Authenticate to GitHub API Client

    :param access_token: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
    :return: github.Github
    """
    g = Github(access_token)
    return g


def save_ci_file(content, ci_sys, repo):
    """

    """
    ci_files = []
    if ci_sys == 'GitHub':
        try:
            for gh_content in repo.get_contents('.github/workflows'):
                with open(results_path + gh_content.name, 'w') as outfile:
                    outfile.write(gh_content.decoded_content.decode('utf-8'))
                ci_files.append(gh_content.decoded_content.decode('utf-8'))
        except:
            # Logging
            pass
    elif ci_sys == 'Travis':
        try:
            with open(results_path + content.name, 'w') as outfile:
                outfile.write(content.decoded_content.decode('utf-8'))
                ci_files.append(content.decoded_content.decode('utf-8'))
        except:
            pass
    else:
        pass
    return ci_files


def crawl(g, project):
    """
    Crawl Repository
    """
    repo = g.get_repo(project)
    contents = repo.get_contents('.')
    ci_files = []
    for content in contents:
        for ci_sys, pattern in cases.items():
            if re.search(pattern, content.name):
                files = save_ci_file(content, ci_sys, repo)
                ci_files.extend(files)
    return ci_files


def load_sec_tools():
    with open('security_patterns.json', 'r') as infile:
        sec_tools = json.load(infile)

    return sec_tools


def find_sec_tools(ci_files, sec_tools):
    tool_in_project = defaultdict(list)
    for ci_file in ci_files:
        content = ci_file.lower()
        for sec_act, tools in sec_tools.items():
            for tool, details in tools.items():
                sec = False
                for pattern in details['Patterns']:
                    if pattern.lower() in content:
                        sec = True
                    
                    if sec:
                        tool_in_project[sec_act].append(tool)
    return tool_in_project



def main():
    # Load Variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Crawl and store CI files
    g = authenticate(access_token=os.getenv('ACCESS_TOKEN'))
    ci_files = crawl(g, 'angrymeir/Server')
    
    sec_tools = load_sec_tools()
    tool_in_project = find_sec_tools(ci_files, sec_tools)
    print(tool_in_project)

if __name__ == '__main__':
    main()
