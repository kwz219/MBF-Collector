import os

from Util.BFGen import recoverBuggyFile
from Utils import readJsonFile,writeJsonFile
def update_context(json_file,fl_json_f):

    pass
def compute_fault_locations(json_file):
    recover_state,tmp_dir,fileformat = recoverBuggyFile(json_file)
    event_id = os.path.basename(json_file).split('.')[0]
    if recover_state == 0:
        print("succeed to patch file"+json_file)
        buggy_file_path = os.path.join(tmp_dir, event_id + '_buggy.' + fileformat)
        fixed_file_path = os.path.join(tmp_dir, event_id + '_fixed.' + fileformat)
        target_file_path = os.path.join(tmp_dir,event_id+'_FL.json')
        parse_fault_location(buggy_file_path,fixed_file_path,target_file_path,fileformat)

        fault_information = readJsonFile(target_file_path)
        original_result = readJsonFile(json_file)
        original_result["context_and_location"] = fault_information
        writeJsonFile(original_result,json_file)
        pass
    else:
        print("failed to patch file "+json_file)
    return recover_state

def parse_fault_location(buggy_file,fix_file,target_position,jar_path,fileformat):

    os.system("java -jar "+jar_path+" "+buggy_file+" "+fix_file+" "+target_position+" "+fileformat)
    pass