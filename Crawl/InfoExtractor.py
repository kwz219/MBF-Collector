import json
import ssl
import urllib

from Entity.BFEntity import BFEntity
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
        # get the dict of repos
        repo_url = event["repo"]["url"]
        ssl._create_default_https_context = ssl._create_unverified_context

        with urllib.request.urlopen(repo_url) as url:
            json_dict = json.loads(url.read().decode())
            repo_language = json_dict["language"]
            repo_stars = json_dict["stargazers_count"]
        bug_fix_entity.init_repo_info(repo_url, repo_stars, repo_language)
    pass

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

def recordPatch(bug_fix_entity:BFEntity,event:dict,event_type:str):
    if event_type=="PushEvent":
        if event.get("payload") is not None:
            # print(event["payload"]["commits"])
            commit_url = event["payload"]["commits"][0]["url"]
        else:
            return None
        ssl._create_default_https_context = ssl._create_unverified_context
        with urllib.request.urlopen(commit_url) as url:
            json_dict = json.loads(url.read().decode())
            files = json_dict["files"]
            raw_url = files[0]["raw_url"]
            patch = files[0]["patch"]
        commit_info = {
            "commit_url": commit_url,
            "fixed_file": raw_url,
            "patch": patch,
        }
        bug_fix_entity.fix_file_code=commit_info["fixed_file"]
        bug_fix_entity.commit_url=commit_info["commit_url"]
        bug_fix_entity.patch = commit_info["patch"]
    return commit_info

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
#test_pushEvent_repoANDmessage()
