from github import Github
from github.GithubObject import NotSet


def get_commit_messages(project, since=None):
    github = Github(project.git_username, project.git_password)
    if not since:
        since = NotSet
    return github.get_user().get_repo(project.git_repo).get_commits(since=since)
