import requests
import os
import Util.Utils as utils



def DownloadEventsFromGitHubArchive(year,month,day,hour,store_dir):
    """
    :param year: year
    :param month: month
    :param day: day
    :param hour: hour
    :param store_dir: the directory which you want to store the json file
    :return: Flag,Address. Flag: whether the download event succeeds, Address: If succeed, return the storage address of the downloaded file.
    """

    year=str(year)
    month = str(month) if month>=10 else '0'+str(month)
    day = str(day) if day>=10 else '0'+str(day)
    hour = str(hour)
    events_info_url = "https://data.gharchive.org/"+"-".join([year,month,day,hour])+".json.gz"
    store_path = os.path.join(store_dir,"-".join([year,month,day,hour])+".json.gz")
    events_file = requests.get(events_info_url)
    open(store_path,'wb').write(events_file.content)
    utils.decompressGZfile(store_path)

def getCompleteCommitInfo(event):
    """

    :param event:
    :return: a dict that stores the complete commit information of a push event
    """

def test_DownloadAndDecompress():
    year=2015
    month=11
    day=1
    hour=23
    store_dir="../temp"
    DownloadEventsFromGitHubArchive(year,month,day,hour,store_dir)

test_DownloadAndDecompress()










