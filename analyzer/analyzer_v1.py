import os
import re
import json
import shutil

from collections import defaultdict
from dotenv import load_dotenv

from github import Github
from github.GithubException import RateLimitExceededException


cases = {'Travis': '.travis.yml', 'GitHub': '.github'}
results_path = './ci_files/'

def prepare_environment():
    exists = os.path.exists(results_path)
    if exists:
        shutil.rmtree(results_path)
    
    os.mkdir(results_path)


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
        except Exception as e:
            print(e)
    elif ci_sys == 'Travis':
        try:
            with open(results_path + content.name, 'w') as outfile:
                outfile.write(content.decoded_content.decode('utf-8'))
                ci_files.append(content.decoded_content.decode('utf-8'))
        except Exception as e:
            print(e)
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
    with open('../resources/tool_patterns.json', 'r') as infile:
        tools = json.load(infile)

    return tools


def find_sec_tools(ci_files, tool_list):
    tool_in_project = defaultdict(list)
    for ci_file in ci_files:
        content = ci_file.lower()
        for act, tools in tool_list.items():
            for tool, details in tools.items():
                usage = False
                for pattern in details['Patterns']:
                    if pattern.lower() in content:
                        usage = True

                    if usage:
                        tool_in_project[act].append(tool)
    return tool_in_project


def main():
    prepare_environment()
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
