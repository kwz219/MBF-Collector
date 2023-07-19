import json
import os


class BFEntity():
    def __init__(self,id,event_type):
        #id github event id
        self.id = id

        # event information
        self.event_type=event_type
        self.commit_url=None

        # bug-fix pair information
        self.buggy_file_code=None
        self.fix_file_info=None
        self.commit_message=None
        self.patch=None
        self.fault_type=None
        self.fault_location=None

        # for deriving original buggy code backwards
        self.raw_fixed_file=None

        # extra information for PullRequest Event
        self.merged = None
        self.issue_url=None
        self.issue_title=None
        self.issue_comments_html = None
        self.issue_comments_body=None

    def init_repo_info(self,repo_url,repo_stars,repo_language,forked_count,license):
        self.repo_url = repo_url
        self.repo_stars = repo_stars
        self.repo_language = repo_language

        self.forked_count = forked_count
        self.license = license

    def print_info(self):
        print("="*10,self.event_type,self.id,"="*10)
        print("Commit Message",self.commit_message)
        print("Repo Information",self.repo_stars,self.repo_language,)
        print("Patch", self.patch)
        #print("Fixed File",self.fix_file_code)

    def save_as_json(self,dir):
        entity_json={}
        if self.event_type=="PushEvent":
            entity_json["event_info"]={"event_id":self.id,
                                       "event_type":self.event_type}
            entity_json["repo"]={"repo_url":self.repo_url,
                                 "stars":self.repo_stars,
                                 "language":self.repo_language,
                                 "forks":self.forked_count,
                                 "license":self.license}
            entity_json["bf_info"]={"buggy_file_content":self.buggy_file_code,
                                    "fix_file_info":self.fix_file_info,
                                    "commit_url":self.commit_url,
                                    "commit_message":self.commit_message,
                                    "patch":self.patch,
                                    "fault_type":self.fault_type,
                                    "fault_location":self.fault_location,
                                    }
            with open(os.path.join(dir,self.id+".json"),'w',encoding='utf8')as f:
                f.write(json.dumps(entity_json,indent=10))
                f.close()
        elif self.event_type == "PullRequestEvent":
            entity_json["event_info"]={"event_id":self.id,
                                       "event_type":self.event_type,
                                       "merged":self.merged}
            entity_json["repo"]={"repo_url":self.repo_url,
                                 "stars":self.repo_stars,
                                 "language":self.repo_language,
                                 "forks":self.forked_count,
                                 "license":self.license}
            entity_json["bf_info"]={"buggy_file_content":self.buggy_file_code,
                                    "fix_file_info":self.fix_file_info,
                                    "commit_url":self.commit_url,
                                    "commit_message":self.commit_message,
                                    "patch":self.patch,
                                    "fault_type":self.fault_type,
                                    "fault_location":self.fault_location,
                                    }
            entity_json["issue_info"]={"issue_url":self.issue_url,
                                       "issue_title":self.issue_title,
                                       "issue_comments_url":self.issue_comments_html,
                                       "issue_comments_content":self.issue_comments_body}
            with open(os.path.join(dir,self.id+".json"),'w',encoding='utf8')as f:
                f.write(json.dumps(entity_json,indent=10))
                f.close()





