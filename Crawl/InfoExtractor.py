import json
import ssl
import urllib

import requests
import Util.Utils as utils
from Entity.BFEntity import BFEntity

def recordRepoInfo(bug_fix_entity:BFEntity,event:dict,event_type:str,au_token:str):
    """
    record the repo info of the event
    :param bug_fix_entity:
    :param event:
    :param event_type: the algorithm may diff by "PushEvent" or "PullRequest"
    :return:
    """
    #bug_fix_entity.init_repo_info(x,x,x)

    if event_type == "PushEvent":
        # get the dict of repos
        repo_url = event["repo"]["url"]
        repo_json = utils.getRequestJsonByGithubAuthentication(repo_url,au_token)
        repo_language = repo_json["language"]
        repo_stars = repo_json["stargazers_count"]

        forks_count = repo_json["forks"]

        if repo_json["license"] == None:
            license_key = None
        else:
            license_key = repo_json["license"]["key"]
        bug_fix_entity.init_repo_info(repo_url, repo_stars, repo_language,forks_count,license_key)
    elif event_type == "PullRequestEvent":
        repo_url = event["repo"]["url"]
        repo = utils.getRequestJsonByGithubAuthentication(repo_url,au_token)

        stars = repo["stargazers_count"]
        language = repo["language"]
        forks_count = repo["forks"]
        if repo["license"] == None:
            license_key = None
        else:
            license_key = repo["license"]["key"]
        bug_fix_entity.init_repo_info(repo_url, stars, language,forks_count,license_key)

def recordCommitMessage(bug_fix_entity:BFEntity,event:dict,event_type:str):
    """
    :param bug_fix_entity:
    :param event:
    :param event_type:
    :return:
    """
    if event_type == "PushEvent":
        if event.get("payload") is not None:
            bug_fix_entity.commit_message = event["payload"]["commits"][0]["message"]
        else:
            bug_fix_entity.commit_message = event["commit"]["message"]
    elif event_type == "PullRequestEvent":
        commits_url = event["payload"]["pull_request"]["commits_url"]
        commits_json = requests.get(commits_url).json()
        commit_message = []
        raw_fixed_file = []
        patch = []
        for commit in commits_json:
            commit_message.append(commit["commit"]["message"])
            commit_info = requests.get(commit["url"] ).json()
            for file in commit_info["files"]:
                raw_fixed_file.append(requests.get(file["raw_url"]).text)
                patch.append(file["patch"])

        bug_fix_entity.commit_message = commit_message
        bug_fix_entity.raw_fixed_file = raw_fixed_file
        bug_fix_entity.patch = patch

def recordCommitInfoforPullRequestEvent(bug_fix_entity:BFEntity,pullrequest_info:dict,au_token):
    commit_infos_json = utils.getRequestJsonByGithubAuthentication(pullrequest_info["commits_url"], au_token)
    commit_info_json =commit_infos_json[0]
    commit_message = commit_info_json["commit"]["message"]
    commit_url = commit_info_json["url"]
    bug_fix_entity.commit_message = commit_message
    bug_fix_entity.commit_url = commit_url
    #print(commit_url)
    commit_json = utils.getRequestJsonByGithubAuthentication(commit_url,au_token)
    #print(commit_json.keys())

    files = commit_json["files"]
    contents_url = files[0]["contents_url"]
    commit_url = commit_json["url"]
    content_json = utils.getRequestJsonByGithubAuthentication(contents_url, au_token)

    patch = files[0]["patch"]

    bug_fix_entity.fix_file_info = {"file_path": content_json["path"], "url": content_json["url"],
                                    "content": content_json["content"], "encoding": content_json["encoding"]}
    bug_fix_entity.commit_url = commit_url
    bug_fix_entity.patch = patch

def recordPatch(bug_fix_entity:BFEntity,commit_json,event_type:str,authen_token:str):
    if event_type=="PushEvent":

        files = commit_json["files"]
        contents_url = files[0]["contents_url"]
        commit_url = commit_json["url"]
        content_json= utils.getRequestJsonByGithubAuthentication(contents_url,authen_token)

        patch = files[0]["patch"]

        bug_fix_entity.fix_file_info={"file_path":content_json["path"],"url":content_json["url"],
                                      "content":content_json["content"],"encoding":content_json["encoding"]}
        bug_fix_entity.commit_url = commit_url
        bug_fix_entity.patch = patch
    elif event_type == "PullRequestEvent":
        pass

def recordIssueInfo(bug_fix_entity:BFEntity,event:dict,au_token):

    api_url = event["payload"]["pull_request"]["issue_url"]

    issue = utils.getRequestJsonByGithubAuthentication(api_url,au_token)

    title = issue["title"]
    comments_url = issue["comments_url"]

    bug_fix_entity.issue_url = api_url
    bug_fix_entity.issue_title = title
    bug_fix_entity.issue_comments_html = comments_url
    bug_fix_entity.issue_comments_body = issue["body"]

def test_pushEvent_repoANDmessage():
    bug_fix_entity = BFEntity()
    with open("../temp/push_event_example.json",'r',encoding='utf8') as f:
        event = json.load(f)
        f.close()
    recordRepoInfo(bug_fix_entity,event,"PushEvent")
    print("repo_url: " + bug_fix_entity.repo_url)
    print("repo_stars: " + str(bug_fix_entity.repo_stars))
    print("repo_language: " + bug_fix_entity.repo_language)
    recordCommitMessage(bug_fix_entity,event,"PushEvent")
    print("commit_message: " + bug_fix_entity.commit_message)

def test_pushEvent_patch():
    bug_fix_entity = BFEntity()
    with open("../temp/push_event_example.json", 'r', encoding='utf8') as f:
        event = json.load(f)
        f.close()
    recordPatch(bug_fix_entity,event,"PushEvent")
    print(bug_fix_entity.patch)
    print(bug_fix_entity.fix_file_code)

"""
def test_PullRequestEvent():
    bug_fix_entity=BFEntity()
    with open("../temp/pullrequest_event_example.json",'r',encoding='utf8')as f:
        event=json.load(f)
        f.close()
    recordRepoInfo(bug_fix_entity,event,"PullRequestEvent")
    print("repo_url: " + bug_fix_entity.repo_url)
    print("repo_stars: " + str(bug_fix_entity.repo_stars))
    print("repo_language: " + bug_fix_entity.repo_language)

    recordCommitMessage(bug_fix_entity,event,"PullRequestEvent")
    print("commit_message: "+bug_fix_entity.commit_message[0])

    #recordPatch(bug_fix_entity, event, "PullRequestEvent")
    #print(bug_fix_entity.patch)
    #print(bug_fix_entity.fix_file_code)

    recordIssueInfo(bug_fix_entity,event,"PullRequestEvent")
    print(bug_fix_entity.issue_url)
    print(bug_fix_entity.issue_title)
    print(bug_fix_entity.issue_comments)

#test_pushEvent_repoANDmessage()
test_PullRequestEvent()
"""
