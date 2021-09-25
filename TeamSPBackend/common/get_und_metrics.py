import understand
import json
import sys
import os

# using Understand for analyze Metrics

# For Mac
# UND_PATH = '/Applications/Understand.app/Contents/MacOS/'
# For Linux Server
UND_PATH = '~/comp90082sp/understand/scitools/bin/linux64/'
# For Windows, you may need to customise it for your Understand installation
# Only customise path before \\SciTools\\bin\\pc-win64
# UND_PATH = 'D:\\SciTools\\bin\\pc-win64'

sys.path.append(UND_PATH)
sys.path.append(UND_PATH+'Python')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# '/home/ec2-user/comp90082sp/COMP90082_Software_Project_Database_Backend/'
UND_FILE_PATH = os.path.dirname(BASE_DIR)
# For Linux or Mac
METRICS_FILE_PATH = BASE_DIR + '/resource/understand/'
# For Windows
# METRICS_FILE_PATH = BASE_DIR + "\\resource\\understand\\"

if __name__ == '__main__':
    und_file_name = sys.argv[1]
    metrics_file_name = sys.argv[2]
    und_file = UND_FILE_PATH + "/" + und_file_name

    # For Linux or Mac
    metrics_file = METRICS_FILE_PATH + metrics_file_name
    # For Windows
    # metrics_file = metrics_file_name

    # print('BASE_DIR : ', BASE_DIR)
    # print('und_file : ', und_file)
    # print('metrics_file : ', metrics_file)
    # open a project und
    udb = understand.open(und_file)
    # get all project metrics
    metrics = udb.metric(udb.metrics())
    # write the metrics result to metrics_file (.json)
    with open(metrics_file, 'w') as fp:
        json.dump(metrics, fp, indent=4)
