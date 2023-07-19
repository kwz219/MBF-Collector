import Util.Utils as utils
from Entity.BFEntity import BFEntity
from Crawl.InfoExtractor import recordRepoInfo, recordCommitMessage, recordPatch, recordIssueInfo
from Crawl.Crawler import getCompleteCommitInfo
def downloadAndDecompress(start_time,end_time):
    """
    download github events from start_time to end_time from github archive
    :param start_time: year-month-day-hour xxxx-xx-xx-x (hour from 0 to 23)
    :param end_time: year-month-day-hour xxxx-xx-xx-x (hour from 0 to 23)
    :return:
    """
    # download github events from github archive



def parseBasicInformation(events_json_f:str, target_types:list,only_single_file_change:bool):
    """
    :param events_json_f: events json downloaded from github archive
    :param target_types: target events types: ["PushEvent","PullRequestEvent"]
    :return: a list of BFEntity: bf-pair with all extracted information
    """

    # 0. init a list of BFEntity (bug-fix entity)
    BFEntities=[]

    # 1. load json file
    events=utils.loadEventsJson(events_json_f)


    # 2. filter events
    # 2.1 filter by event types: PushEvent, PullRequestEvent
    # 2.2 filter by keywords from MESSAGE: bug, fix, repair.... (综合一下之前的方法都用的什么，可能需要正则匹配)
    target_type_events = utils.filterEventsByTypes(events,["PushEvent","PullRequestEvent"])
    bug_fix_events = utils.filterEventsByKeywords(target_type_events)

    # 3. Traverse each event
    # 3.1 get repo information of each event (language, repo address)
    # 3.2 get COMMIT MESSAGE
    # 3.3 get complete commit information through the commit url
    for event in bug_fix_events:
        bug_fix_entity= BFEntity()
        if event["type"]=="PushEvent":
            recordRepoInfo(bug_fix_entity,event,"PushEvent")
            recordCommitMessage(bug_fix_entity,event,"PushEvent")
            # 4.  through the commit url, get raw FIX FILE, PATCH
            recordPatch(bug_fix_entity,event,"PushEvent")
            pass
        elif event["type"]=="PullRequestEvent":

            recordRepoInfo(bug_fix_entity, event, "PullRequestEvent")
            recordCommitMessage(bug_fix_entity, event, "PullRequestEvent")
            recordIssueInfo(bug_fix_entity, event)
            recordPatch(bug_fix_entity,event,"PullRequestEvent")
            pass



        # 4.  through the commit url, get raw FIX FILE, PATCH

        # 5.  get FAULT LOCATION, BUGGY CODE WITH CONTEXT, FIX CODE by analyzing FIX FILE and PATCH
          #TODO 戈

        # 6. get FAULT TYPE by analyzing COMMIT MESSAGE

        # 7. store all information of current commit-event
    pass