
def count_fault_by_type_log(logs_path):
    push_events_count={}
    pr_events_count={}
    for log_path in logs_path:
        print(log_path)
        with open(log_path,'r',encoding='utf8')as f:
            for line in f:
                infos = line.strip().split('\t')
                path=infos[0]
                #print(path)
                language=infos[2]
                if "PushEvent" in path:
                    if language in push_events_count.keys():
                        push_events_count[language]=push_events_count[language]+1
                    else:
                        push_events_count[language] = 1
                elif "PREvent" in path:
                    if language in pr_events_count.keys():
                        pr_events_count[language] = pr_events_count[language] + 1
                    else:
                        pr_events_count[language] = 1
            f.close()
    print("push",push_events_count)

    print("pull request",pr_events_count)
    pass
count_fault_by_type_log(["/home/zwk/BF_DATA/2020-7-type.log",
                         "/home/zwk/BF_DATA/2020-8-type.log",
                         "/home/zwk/BF_DATA/2020-9-type.log",
                         "/home/zwk/BF_DATA/2020-4/2020-4-type.log",
                         "/home/zwk/BF_DATA/2020-4/2020-5-type.log",
                         "/home/zwk/BF_DATA/2020-4/2020-6-type.log",
                         "/home/zwk/BF_DATA/2020-3-type.log",
                         "/home/zwk/BF_DATA/2020-2-type.log",
                         "/home/zwk/BF_DATA/2020-1-type.log"])