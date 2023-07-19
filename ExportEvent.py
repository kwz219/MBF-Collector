import json
import os
import csv
import xlsxwriter
def exportMessage(dir,output_path):
    files=os.listdir(dir)
    result_list=[]
    workbook = xlsxwriter.Workbook(output_path,options={'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    for f in files:
        if f.endswith(".json"):
            result=None
            with open(os.path.join(dir,f),'r',encoding='utf8')as jf:
                result = json.load(jf)
                jf.close()
            id = result["event_info"]["event_id"]
            commit_message = result["bf_info"]["commit_message"]
            patch = result["bf_info"]["patch"]
            if len(commit_message.split())>2:
                result_list.append([id,patch,commit_message])

    for i,re in enumerate(result_list):
        for j,col in enumerate(re):
            worksheet.write(i,j,col)
    workbook.close()

def exportPRMessage(dir,output_path):
    files=os.listdir(dir)
    result_list=[]
    workbook = xlsxwriter.Workbook(output_path,options={'nan_inf_to_errors': True})
    worksheet = workbook.add_worksheet()
    for f in files:
        if f.endswith(".json"):
            result=None
            with open(os.path.join(dir,f),'r',encoding='utf8')as jf:
                result = json.load(jf)
                jf.close()
            id = result["event_info"]["event_id"]
            print(id,result.keys())
            commit_message = result["bf_info"]["commit_message"]
            patch = result["bf_info"]["patch"]
            issue_title = result["issue_info"]["issue_title"]
            issue_comment = result["issue_info"]["issue_comments_content"]
            if len(commit_message.split())>2:
                result_list.append([id,patch,issue_title,issue_comment,commit_message])

    for i,re in enumerate(result_list):
        for j,col in enumerate(re):
            worksheet.write(i,j,col)
    workbook.close()
#exportMessage("/home/zwk/BF_DATA/2020-2/2020-02-04-22/PushEvent","/home/zwk/BF_DATA/2020-2/2020-02-04-22/push_event_message.xlsx")
exportPRMessage("/home/zwk/BF_DATA/2020-2/2020-02-13-11/PREvent","/home/zwk/BF_DATA/2020-2/2020-02-13-11/pr_event_message.xlsx")