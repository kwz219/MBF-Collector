import json
import gzip

import requests


def downloadFile(url,location):
    events_file = requests.get(url)
    open(location, 'wb').write(events_file.content)

def decompressGZfile(events_gz_file:str):
    """
    :param events_json_file: the location of the json file year-month-day-hour.json.gz
    """
    f_name = events_gz_file.replace(".gz","")
    g_file = gzip.GzipFile(events_gz_file)
    open(f_name,"wb+").write(g_file.read())
    g_file.close()


def loadEventsJson(events_json_file:str):
    """
    :param events_json_file: the path of the decompressed events json
    :return: all events: [dict,dict,dict......]
    """
    events=[]
    with open(events_json_file,'r',encoding='utf8')as f:
        for line in f:
            events.append(json.loads(line.strip()))
        f.close()
    return events


def filterEventsByTypes(events:list,target_types:list):
    """
    :param events: all events [event:dict,event:dict,event:dict......]
    :param target_types: types of events need to be reserved
    :return: filtered events list
    """
    filtered_events=[]
    for event in  events:
        if 'type' in event.keys():
            if event['type'] in target_types:
                filtered_events.append(event)
    return filtered_events

def filterEventsByKeywords(events:list):
    #TODO
    """
    :param events: [dict,dict,dict]
    :return: filtered events that match the bug-fix keywords
    """
    pass

def test_filterEventsByTypes():
    events_json_path='../temp/2022-01-01-0.json'
    events = loadEventsJson(events_json_path)
    target_types=["PushEvent","PullRequestEvent"]
    filteredEvents = filterEventsByTypes(events,target_types)
    for event in filteredEvents:
        assert event['type'] in target_types
    print(len(filteredEvents))


#test_filterEventsByTypes()
