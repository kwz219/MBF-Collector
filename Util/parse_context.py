from Util.BFGen import recoverBuggyFile
def compute_fault_locations(json_file):
    recover_state = recoverBuggyFile(json_file)
    if recover_state == 0:
        print("succeed to patch file"+json_file)
        pass
    else:
        print("failed to patch file "+json_file)
    return recover_state

def parse_fault_location(buggy_file,fix_file,target_position,jar_path):

    pass