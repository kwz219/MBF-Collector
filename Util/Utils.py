import csv
import json
import gzip
import os
import re
import time

import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

languages = {
	'C': ['.c', '.h'],
	'C++': ['.cpp', '.hpp'],
	'Java': ['.java', '.class', '.jar'],
	'Python': ['.py', '.pyc', '.pyd', '.pys', '.pyx'],
	'JavaScript': ['.js', '.json', '.jsx', '.jsm', 'json5', 'jsonc'],
	'Go': ['.go'],
	'Swift': ['.swift'],
	'Kotlin': ['.kt', '.kts'],
	'YAML': ['.yaml', '.yml'],
	'Ruby': ['.ruby', '.rb'],
	'HTML': ['.html', '.htm', '.xhtml', 'html5'],
	'C#': ['.cs'],
	'MarkDown': ['.md', '.markdown'],
	'PHP': ['.php', '.phtml', '.php3'],
	'NoFileUpdate': ['null'],
	'TypeScript': ['.ts'],
	'Bash': ['.sh', '.bash'],
	'Rust': ['.rs'],
	'Gradle': ['.gradle'],
	'Assemble': ['.asm', '.s', '.inc', '.masm'],
	'Bat': ['.bat'],
	'Cmake/Makefile': ['.cmake', '.make', '.makefile'],
	'Groovy': ['.groovy'],
	'Python Notebook': ['.ipynb']
	# .tf .tsx
}

def getRequestJsonByGithubAuthentication(url,authen_token):
    headers = {"Authorization": 'token '+authen_token}
    content = requests.get(url, headers=headers).json()
    return content

def getRequestContentByGithubAuthetication(url,authen_token):
    headers = {"Authorization": 'token '+authen_token}
    file_content = requests.get(url, headers=headers).content.decode('utf8')
    return file_content

def downloadFile(url,location):
    events_file = requests.get(url)
    open(location, 'wb').write(events_file.content)

def download_by_month(year,month,folder_path):
    if not os.path.exists(folder_path):
        os.system("mkdir "+folder_path)
    os.chdir(folder_path)
    os.system("wget https://data.gharchive.org/"+str(year)+"-"+str(month)+"-{01..31}-{0..23}.json.gz")

def unzip_and_delete_all(folder_path):
    files=os.listdir(folder_path)
    for file in files:
        if file.endswith(".tar.gz"):
            file_path = os.path.join(folder_path,file)
            os.system("tar xzvf "+file_path)
            time.sleep(3)
            os.system("rm "+file_path)
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

def hasBugFixKeywords(message,keywords=["bug","fix","repair","error","defect","issue","mistake","patch","incorrect","fault"]):
    message=str(message).lower()
    for word in keywords:
        if word in message:
            return True
    return False




def test_filterEventsByTypes():
    events_json_path='../temp/2022-01-01-0.json'
    events = loadEventsJson(events_json_path)
    target_types=["PushEvent","PullRequestEvent"]
    filteredEvents = filterEventsByTypes(events,target_types)
    for event in filteredEvents:
        assert event['type'] in target_types
    print(len(filteredEvents))

def judge_language(file_name):
    file_name=str(file_name).lower()
    file_ext = '.'+file_name.split(".")[-1]
    for language, exts in languages.items():
        #print(language,exts)
        if file_ext in exts:
            return language
    return "Unknown"

def find_type_filtered(file_path,id_list):
    with open(file_path, 'r',encoding='utf8') as file:
        data = json.load(file)
        message = data["bf_info"]["commit_message"]
        # 按照关键词提取
        fault_type = matchType_by_key(message)
        file_name = data["bf_info"]["fix_file_info"]["file_path"]
        if not matchType(fault_type,id_list):
            fault_type="Undefined"

        data["bf_info"]["fault_type"] = fault_type.strip()
        # # 直接与类型名称进行cosine相似度比较
        # data["bf_info"]["fault_type"] = match_by_name(message)
    info_id = data["event_info"]["event_id"]
    if fault_type=="Undefined" :
        #print(file_path+" no type find "+info_id)
        return False,fault_type,file_name
    else:
        #print(file_path+" "+data["bf_info"]["fault_type"]+info_id)

        with open(file_path, 'w',encoding='utf8') as f:
            json.dump(data, f, indent=4)
        return True,fault_type,file_name


def loose_match(key, message):
    message = re.sub('[^a-zA-Z0-9\s]+', '', message)
    message = message.strip().lower()
    # 将 key 中的单词按空格进行分割，生成一个单词列表
    words = key.split(' ')

    # 检查单词列表中的每个单词是否都在 message 中出现过
    all_words_in_message = all(word in message for word in words)
    return all_words_in_message

def matchType_by_key(message):
    type_list = []
    # 取一个第二列为每个错误类型key words的csv文件
    file_name = "./Resource/CWE_auto_weak.csv"
    with open(file_name, 'r') as f:
        reader = csv.reader(f)

        # 跳过表头
        next(reader)

        # 循环遍历第二列并读取其中的值
        for row in reader:
            # 取每行对应Key Words列的值
            key = row[1]
            keys = key.split(',')
            keys = [key.strip() for key in keys]
            for key in keys:
                if len(key) == 0:
                    continue
                if loose_match(key, message):
                    type_list.append(row[2])

        if len(type_list) > 1:
            # 用 CountVectorizer 将 message 和 CSV 文件中的每个字符串转化为向量
            vectorizer = CountVectorizer().fit_transform([message, *type_list])

            # 计算 message 与 CSV 文件中每个字符串之间的相似度
            similarities = cosine_similarity(vectorizer)[0][1:]

            # 获取与 message 最相似的字符串
            fault_type = type_list[similarities.argmax()]
            return fault_type
        elif len(type_list) == 1:
            return type_list[0]
        return "UnDefined"

def getCWEmap(file_path="Resource/CWE-analysis-base.csv"):
    lines=[]
    map={}
    with open(file_path,'r',encoding='utf8')as f:
        for line in f:
            lines.append(line.strip())
        f.close()
    for line in lines[1:]:
        infos = line.split(',')
        map[infos[1]]=int(infos[0])
    return map

def matchType(type,id_list):
    map = getCWEmap()
    #print(map.keys())
    map["UnDefined"]=-1
    map['Improper Validation of Specified Index, Position, or Offset in Input']=1285
    map['Reusing a Nonce, Key Pair in Encryption']=323
    map['Use of Hard-coded, Security-relevant Constants']=547
    map['Incorrect Decoding of Security Identifiers']=1290
    if type in map.keys():
        type_id = map[type]
        if type_id in id_list:
            return True
    return False

def readJsonFile(json_f):
    with open(json_f,'r',encoding='utf8')as f:
        result = json.load(f)
    return result

def writeJsonFile(content,json_f):
    with open(json_f,'w',encoding='utf8')as f:
        json.dump(content,f,indent=10)

#test_filterEventsByTypes()

