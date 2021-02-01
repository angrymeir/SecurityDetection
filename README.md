# SecurityDetection
Detect tool usage in a project.

## How does it work?
1. The analyzer takes a GitHub access token from the `.env` file.
2. It then crawls the specified project for CI files.
3. For each CI file it checks for the occurrences of tool patterns.

## Demo
For demo purposes we analyze the following project: https://github.com/angrymeir/server
