import os
import subprocess
import time

from Util.BFGen import recoverBuggyFile
from Util.Utils import readJsonFile,writeJsonFile
def update_context(json_file,fl_json_f):

    pass
def compute_fault_locations(json_file,jar_path):
    recover_state,tmp_dir,fileformat = recoverBuggyFile(json_file)
    event_id = os.path.basename(json_file).split('.')[0]
    skip_list=["11891956296"]
    if recover_state == 0:
        print("succeed to patch file"+json_file)

        if fileformat in ["java","py","cs","cpp","c","js"]:

            buggy_file_path = os.path.join(tmp_dir, event_id + '_buggy.' + fileformat)
            fixed_file_path = os.path.join(tmp_dir, event_id + '_fixed.' + fileformat)
            target_file_path = os.path.join(tmp_dir,event_id+'_FL.json')
            if not os.path.exists(target_file_path) and (not event_id in skip_list):
                if True:
                    state=parse_fault_location(buggy_file_path,fixed_file_path,target_file_path,jar_path,fileformat)
                    if state==0:
                        fault_information = readJsonFile(target_file_path)
                        original_result = readJsonFile(json_file)
                        original_result["context_and_location"] = fault_information
                        writeJsonFile(original_result,json_file)
                #except:
                    #print("failed at fl ",json_file)

        pass
    else:
        print("failed to patch file "+json_file)
    return recover_state

def parse_fault_location(buggy_file,fix_file,target_position,jar_path,fileformat):
    cmd = "java -jar "+jar_path+" "+buggy_file+" "+fix_file+" "+target_position+" "+fileformat
    print(cmd)
    parseProcess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #os.system("java -jar "+jar_path+" "+buggy_file+" "+fix_file+" "+target_position+" "+fileformat)
    begin_time = time.time()
    state=0
    while True:
        state = parseProcess.poll()
        if state == 0:
            print('Successfully parse ' + target_position)
            break
        elif state!=0 and state is not None:
            print('Failed to parse:',target_position)
            #print(state)
            #print(parseProcess.stderr,parseProcess.stdout)
            break
        else:
            time.sleep(1)
        if time.time() - begin_time > 8:
            # if timeout, then terminate the process
            parseProcess.terminate()
            break
    return state