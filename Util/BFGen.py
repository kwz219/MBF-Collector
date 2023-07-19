from enum import Flag
import json
import base64
import subprocess
import time
import os

def getBFfiles(dragFile):
    """
    Through the commit url get fixed file and patch
    :dargFile: commit url json file
    :return: content of fixed file,  patch string, file format(like js, py, java, c, cpp, etc)
    """
    patch = ''
    content = ''
    with open(dragFile, 'r') as f:
        data = json.load(f)
        patch = data['bf_info']['patch']
        content = base64.b64decode(data['bf_info']['fix_file_info']['content']).decode('utf-8')

        fileFormat = os.path.basename(data['bf_info']['fix_file_info']['file_path']).split(".")[-1]
    return content, patch, fileFormat

def writeFile(content,file_path):
    with open(file_path,'w',encoding='utf8')as f:
        f.write(content)
        f.close()

def recoverBuggyFile(json_path):
    fix_file_content,patch_content,fileformat = getBFfiles(json_path)
    event_id = os.path.basename(json_path).split('.')[0]
    tmp_dir = json_path.replace(".json","")+"_BFcontents"
    if not os.path.exists(tmp_dir):
        os.system("mkdir "+tmp_dir)
    else:
        return -1
    buggy_file_path = os.path.join(tmp_dir,event_id+'_buggy.'+fileformat)
    fixed_file_path = os.path.join(tmp_dir,event_id+'_fixed.'+fileformat)
    patch_path = os.path.join(tmp_dir,event_id+".patch")
    writeFile(fix_file_content,buggy_file_path)
    writeFile(fix_file_content,fixed_file_path)
    writeFile(patch_content,patch_path)
    patchInstruction = 'patch -R ' + buggy_file_path + ' ' + patch_path
    #print(patchInstruction)
    diffProcess = subprocess.Popen(patchInstruction, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    state = 0
    begin_time = time.time()

    # with open('../temp/log.txt', 'w') as log:
    while True:
        state = diffProcess.poll()
        if state == 0:
            #print('Successfully recover the fixed file into buggy file ' + json_path)
            break
        elif state != 0 and state is not None:
            #print('File Recover Failed: ' + event_id)
            break
        elif time.time() - begin_time > 2:
            # if timeout, then terminate the process
            diffProcess.terminate()
            break
        else:
            time.sleep(1)
    return state,tmp_dir,fileformat

def recoverFault(jsonFile):
    """
    Recover the buggy file, use 'diff' / 'patch' instruction in linux
    :jsonFile: string, path of json file crawled in step3
    Associate the folder as followed
    temp
    |
    |----buggyFile: the buggy file with code format
    |----fixFile: the fixed file content with code format
    |----patch: .patch file that is recovered using 'patch' instruction in linux
    """
    content, patch, fileForamt = getBFfiles(jsonFile)
    
    fileName = os.path.basename(jsonFile).split('.')[0]
    
    with open('../temp/buggyFile/' + fileName + '.' + fileForamt, 'w') as f:
        f.write(content)
    with open('../temp/fixedFile/' + fileName + '.' + fileForamt, 'w') as f:
        f.write(content)
    with open('../temp/patch/' + fileName + '.' + 'patch', 'w') as f:
        f.write(patch)
    patchInstruction = 'patch -R ../temp/buggyFile/' + fileName + '.' + fileForamt +' ../temp/patch/' + fileName + '.patch'

    diffProcess = subprocess.Popen(patchInstruction, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    state = 0
    begin_time = time.time()

    # with open('../temp/log.txt', 'w') as log:
    while True:
        state = diffProcess.poll()
        if state == 0:
            print('Successfully recover the fixed file into buggy file ' + fileName)
            break
        elif state != 0 and state is not None:
            print('File Recover Failed: ' + fileName) 
            break
        elif time.time() - begin_time > 2:
            # if timeout, then terminate the process
            diffProcess.terminate()
            break
        else:
            time.sleep(1)
    return state

def constructBF(crawledFolder):
    """
    construct BF files in folder, for example '2020-02-04-1/PREvent/'
    """
    files = os.listdir(crawledFolder)
    for i in files:
        recoverFault(crawledFolder + i)
#recoverBuggyFile("/home/zwk/BF_DATA/2020-2/2020-02-04-9/PushEvent/11429881907.json")