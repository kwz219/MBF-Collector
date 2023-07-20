import os

import Util.Utils as utils
import logging
from logging.handlers import RotatingFileHandler
from Entity.BFEntity import BFEntity
from Crawl.InfoExtractor import recordRepoInfo,recordPatch,recordCommitInfoforPullRequestEvent,recordIssueInfo

def setupLogger(log_file_path):
    logger = logging.getLogger(log_file_path.replace(".json",""))
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    fh = logging.handlers.TimedRotatingFileHandler(
        filename=log_file_path,
        encoding='utf-8')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
def process_json_file(json_file_path,logger,au_token,pushevent_save_dir,prevent_save_dir):
    all_events=utils.loadEventsJson(json_file_path)
    succeed_count=0
    error_count=0
    skipped_count=0

    for idx,event in enumerate(all_events):
        changed_files=[]
        event_type = event["type"]
        id = event["id"]
        bug_fix_entity=None
        if idx%100==0:
            logger.info("Statistics: "+" Succeed: "+str(succeed_count)+" Skip: "+str(skipped_count)+" Error: "+str(error_count))
        # record info of push event
        if event_type == "PushEvent":
            login_name = event["actor"]["login"]

            # skip events acted by bots
            if "[bot]" in login_name:
                logger.info("SKIP PushEvent "+id+" #Reason Actor Bot")
                skipped_count+=1
            else:
                if "payload" in event.keys():
                    commits = event["payload"]["commits"]
                    #print(commits)
                    if len(commits)>1 or len(commits)==0:
                        logger.info("SKIP PushEvent " + id + " #Reason More than one commits in the event")
                        skipped_count += 1
                    else:
                        commit=commits[0]
                        message = commit["message"]
                        if(utils.hasBugFixKeywords(message)):
                            logger.info(
                                "FIND PushEvent " + id + " #Message "+str(message).replace('\n',''))
                            #(commit['url'])
                            try:
                                commit_dict = utils.getRequestJsonByGithubAuthentication(commit["url"],au_token)
                            except:
                                logger.info(
                                    "ERROR PushEvent " + id + " when getting commit information")
                                error_count += 1
                                continue
                            if "files" in commit_dict.keys():
                                changed_files = commit_dict["files"]
                            else:
                                logger.info(
                                    "SKIP PushEvent " + id + " #Reason No file changed")
                                skipped_count += 1
                                continue
                            if len(changed_files)>1:
                                logger.info(
                                    "SKIP PushEvent " + id + " #Reason More than one file changed")
                                skipped_count += 1
                            else:
                                bug_fix_entity = BFEntity(id,event_type)

                                # record basic information
                                try:
                                    status=recordPatch(bug_fix_entity,commit_dict,"PushEvent",au_token)
                                    if status in ["No Raw URL","Decode Error"]:
                                        logger.info(
                                            "SKIP PushEvent " + id + " #Reason "+status)
                                        skipped_count += 1
                                    else:
                                        repo_status=recordRepoInfo(bug_fix_entity, event, "PushEvent", au_token)
                                        if repo_status in ["No Repo Information"]:
                                            logger.info(
                                                "SKIP PushEvent " + id + " #Reason " + repo_status)
                                            skipped_count += 1
                                        else:
                                            bug_fix_entity.commit_message = message
                                            logger.info(
                                                "SUCCEED PushEvent " + id )
                                            succeed_count+=1
                                            bug_fix_entity.print_info()
                                            bug_fix_entity.save_as_json(pushevent_save_dir)
                                except:
                                    logger.info(
                                        "ERROR PushEvent " + id + " when parsing basic information")
                                    error_count += 1
                        else:
                            logger.info("SKIP PushEvent "+id + " #Reason The commit message does not contain bug-fix keywords" )
                            skipped_count += 1
                else:
                    logger.info("SKIP PushEvent " + id + " #Reason No Payload Information")
                    skipped_count += 1

                pass

        # record info of pull request event
        elif event_type == "PullRequestEvent":
            login_name = event["actor"]["login"]

            # skip events acted by bots
            if "[bot]" in login_name:
                logger.info("SKIP PullRequestEvent " + id + " #Reason Actor Bot")
                skipped_count += 1
            else:
                if "payload" in event.keys():

                    if not "pull_request" in event["payload"].keys():
                        #print(id, event["payload"].keys())
                        logger.info("SKIP PullRequestEvent " + id + " #Reason No PullRequest Information")
                        skipped_count += 1
                        continue

                    pullrequest_info = event["payload"]["pull_request"]
                    #print(id, pullrequest_info.keys())
                    commits_num = pullrequest_info["commits"]
                    changed_files_num = pullrequest_info["changed_files"]
                    if not commits_num == 1:
                        logger.info("SKIP PullRequestEvent " + id + " #Reason More than one commit")
                        skipped_count += 1
                        continue
                    elif not changed_files_num == 1:
                        logger.info("SKIP PullRequestEvent " + id + " #Reason More than one file changed")
                        skipped_count += 1
                        continue
                    else:
                        try:
                            pr_title = pullrequest_info["title"]
                            if utils.hasBugFixKeywords(pr_title):
                                logger.info("FIND PullRequestEvent "+id+ " #Title "+pr_title)
                            else:
                                logger.info("SKIP PullRequestEvent " + id + " #Reason More than one file changed")
                                skipped_count+=1
                                continue
                            bug_fix_entity = BFEntity(id, event_type)
                            bug_fix_entity.merged=pullrequest_info["merged"]
                            recordRepoInfo(bug_fix_entity,event,"PullRequestEvent",au_token)
                            recordCommitInfoforPullRequestEvent(bug_fix_entity,pullrequest_info,au_token)
                            recordIssueInfo(bug_fix_entity,event,au_token)
                            bug_fix_entity.save_as_json(prevent_save_dir)
                            #print("saved",id)
                            succeed_count+=1
                        except:
                            logger.info(
                                "ERROR PullRequestEvent " + id + " when parsing basic information")
                            error_count += 1

                    pass
                else:
                    logger.info("SKIP PullRequestEvent " + id + " #Reason No Payload Information")
                    skipped_count += 1
        else:
            logger.info("SKIP Event " + id + " #Reason Type "+event_type)

def main():
    jsons_dir = "/home/zwk/GA_Data/2020/2"
    files=os.listdir(jsons_dir)
    save_root_dir = "/home/zwk/BF_DATA/2020-2"

    au_token = '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'
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(jsons_dir,file)
            log_path = os.path.join(save_root_dir,file.replace(".json",".crawl.log"))
            if os.path.exists(log_path):
                continue
            save_dir = os.path.join(save_root_dir,file.replace(".json",""))
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            push_save_dir = os.path.join(save_dir,"PushEvent")
            pr_save_dir = os.path.join(save_dir,"PREvent")
            if not os.path.exists(push_save_dir):
                os.mkdir(push_save_dir)
            if not os.path.exists(pr_save_dir):
                os.mkdir(pr_save_dir)
            logger = setupLogger(log_path)
            process_json_file(file_path, logger, au_token, push_save_dir,pr_save_dir)

main()