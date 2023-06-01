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
    pass

def recordCommitMessage(bug_fix_entity:BFEntity,event:dict,event_type:str):
    """
    :param bug_fix_entity:
    :param event:
    :param event_type:
    :return:
    """
    #bug_fix_entity.commit_message=

