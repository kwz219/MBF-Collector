from sqlalchemy import true, false, null

from Entity.BFEntity import BFEntity
import requests
headers = {'Authorization': 'YOUR_TOKEN'}


def recordRepoInfo(bug_fix_entity:BFEntity,event:dict,event_type:str):
    """
    record the repo info of the event
    :param bug_fix_entity:
    :param event:
    :param event_type: the algorithm may diff by "PushEvent" or "PullRequest"
    :return:
    """
    #bug_fix_entity.init_repo_info(x,x,x)
    if event_type == "PushEvent":
        pass
    else:
        api_url = event["repo"]["url"]
        repo = requests.get(api_url,headers=headers).json()
        url = repo["html_url"]
        stars = repo["stargazers_count"]
        language = repo["language"]
        bug_fix_entity.init_repo_info(url, stars, language)


def recordCommitMessage(bug_fix_entity:BFEntity,event:dict,event_type:str):
    """
    :param bug_fix_entity:
    :param event:
    :param event_type:
    :return:
    """
    #bug_fix_entity.commit_message=
    if event_type == "PushEvent":
        pass
    else:
        commits_url = event["payload"]["pull_request"]["commits_url"]
        commits_json = requests.get(commits_url,headers=headers).json()
        commit_message = []
        raw_fixed_file = []
        patch = []
        for commit in commits_json:
            commit_message.append(commit["commit"]["message"])
            commit_info = requests.get(commit["url"],headers=headers).json()
            for file in commit_info["files"]:
                raw_fixed_file.append(requests.get(file["raw_url"],headers=headers).text)
                patch.append(file["patch"])

        bug_fix_entity.commit_message = commit_message
        bug_fix_entity.raw_fixed_file = raw_fixed_file
        bug_fix_entity.patch = patch


def recordIssueInfo(bug_fix_entity:BFEntity, event:dict):
    api_url = event["payload"]["pull_request"]["issue_url"]
    response = requests.get(api_url,headers=headers)
    issue = response.json()
    url = issue["html_url"]
    title = issue["title"]
    comments_url = issue["comments_url"]
    comments = requests.get(comments_url,headers=headers).json()
    bug_fix_entity.issue_url = url
    bug_fix_entity.issue_title = title
    bug_fix_entity.issue_comments = comments
