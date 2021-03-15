# SecurityDetection
Detect tool usage in a project.

## How does it work?
1. The analyzer takes a GitHub access token from the `.env` file.
2. It then crawls the specified project for CI files.
3. For each CI file it checks for the occurrences of tool patterns.

## Demo
For demo purposes we analyze the following project: https://github.com/angrymeir/server

### Status of Demo
| Activity | Tool | Activity detected by analyzer | Artifact stored in external repository | Analyzer V1 | Analyzer V2  | Support | Prec/Rec/F1 |
|:---------|:------|:----------------------------:|:--------------------------------------:|:-----------------------------:|:--------------------:|:----:|:----:|
| Static Code Analysis | Bandit | X | - | X | X | 2360 | 1.0/0.99/0.99 |
| Third Party Library | CycloneDX | X | - | X | X | 424 | 0.94/1.0/0.97 |
| Unit Test | PyTest | X | - | X | X | 16 | 1.0/1.0/1.0 |
