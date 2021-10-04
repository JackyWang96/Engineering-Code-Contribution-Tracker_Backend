import understand
import json
import sys
import os

# using Understand for analyze Metrics

# For Mac
# UND_PATH = '/Applications/Understand.app/Contents/MacOS/'

# For Linux Server
#UND_PATH = '~/comp90082sp/understand/scitools/bin/linux64/'

# For Windows
UND_PATH = 'E:\\kimchy\\SciTools\\bin\\pc-win64'

sys.path.append(UND_PATH)
sys.path.append(UND_PATH+'Python')

# '/home/ec2-user/comp90082sp/COMP90082_Software_Project_Database_Backend/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UND_FILE_PATH = os.path.dirname(BASE_DIR)
# METRICS_FILE_PATH = BASE_DIR + '/resource/understand/'
METRICS_FILE_PATH = BASE_DIR + "\\resource\\understand\\"


if __name__ == '__main__':
    und_file_name = sys.argv[1]
    metrics_file_name = sys.argv[2]
    und_file = UND_FILE_PATH + "/" + und_file_name
    # metrics_file = METRICS_FILE_PATH + metrics_file_name
    metrics_file = metrics_file_name

    # print('BASE_DIR : ', BASE_DIR)
    # print('und_file : ', und_file)
    # print('metrics_file : ', metrics_file)
    # open a project und
    udb = understand.open(und_file)
    list = []
    for file in udb.ents("File"):
        name = file.longname()
        if UND_FILE_PATH not in name:
            continue
        metric = file.metric(file.metrics())
        if metric:
            dict = {
                "filename": name,
                # "lala": metrics_file
                "attribute": metric
            }
            list.append(dict)
        # metrics = udb.metric(udb.metrics())
        # for k, v in sorted(metrics.items()):
        #     list.append(k, "=", v)
        # print (k,"=",v)
    # get all project metrics
    metrics = udb.metric(udb.metrics())
    # write the metrics result to metrics_file (.json)
    with open(metrics_file, 'w') as fp:
        json.dump(list, fp, indent=4)
