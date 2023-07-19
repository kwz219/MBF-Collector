# the folder contains a list of json files
import os
import os.path
from Util.Utils import find_type_filtered, judge_language
from Util.parse_context import compute_fault_locations

def infer_type_folder(folder_path,id_list,log_f):
    events= ["PushEvent","PREvent"]
    for event in events:
        sub_folder_path = folder_path+'/'+event
        files = os.listdir(sub_folder_path)
        for file in files:
            id = file.replace(".json","")
            json_path = os.path.join(sub_folder_path,file)
            result,type,file_name=find_type_filtered(json_path,id_list)
            if(result):
                language = judge_language(file_name)
                with open(log_f,'a',encoding='utf8')as f:
                    f.write(json_path+'\t'+id+'\t'+language+'\t'+type+'\t'+str(result)+'\n')
                    print(json_path+'\t'+id+'\t'+language+'\t'+type+'\t'+str(result)+'\n')

# traverse for infering types
def traverse_folder_month_infer(month_dir,log_f):
    id_list=[20,120,131,170,172,178,202,248,287,299,362,369,402,476,477,665,704,833,1047,1113,1114]
    dirs = os.listdir(month_dir)
    #print(dirs)
    for dir in dirs:
        sub_dir = os.path.join(month_dir,dir)
        if os.path.isdir(sub_dir):
            print(dir)
            infer_type_folder(sub_dir,id_list,log_f)

#traverse folder for parsing contexts
def traverse_folder_month_parse(month_dir,log_f):
    dirs=os.listdir(month_dir)
    success_count=0
    failed_count=0
    for dir in dirs:
        sub_dir = os.path.join(month_dir,dir)
        if os.path.isdir(sub_dir):
            for event_dir in ["PushEvent","PREvent"]:
                events_dir = os.path.join(sub_dir,event_dir)
                files = os.listdir(events_dir)
                for idx,file in enumerate(files):
                    if file.endswith(".json"):
                        file_path = os.path.join(events_dir,file)
                        state=compute_fault_locations(file_path)
                        if idx%50==0:
                            print("Succeed",success_count,"Failed",failed_count)
                        if state == 0:
                            success_count+=1
                            with open(log_f,'a',encoding='utf8')as f:
                                f.write(file_path+'\t'+"Succeed "+'\n')

                        else:
                            failed_count+=1
                            with open(log_f,'a',encoding='utf8')as f:
                                f.write(file_path+'\t'+"Failed "+'\n')
    pass
