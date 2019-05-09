from github import Github


def get_commit_messages(project):
    commit_messages = []
    github = Github(project.git_username, project.git_password)
    for commit in github.get_user().get_repo(project.git_repo).get_commits():
        commit_messages.append(commit.commit.message)
    return commit_messages
