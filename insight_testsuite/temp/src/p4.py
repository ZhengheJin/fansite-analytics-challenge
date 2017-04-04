#line = '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'
#regex = '(\S*?) - - \[(.*?)\] "[GET,POST] [(\S*?)\s*]+" (\d+?) ([\d+,-])'
#f_in = open('../log_input/log.txt', 'r', encoding='iso-8859-1')
#f_out = open('../log_output/res1.txt', 'w')
	
import io
import queue as Q   # consider using collections.deque(), which requires no package installation
from datetime import datetime, timedelta

f_out = open('../log_output/blocked.txt', 'w', encoding = 'iso-8859-1')

out = set()
warning = dict()
with io.open('../log_input/log.txt', 'r', encoding='iso-8859-1') as f_in:
    for line in f_in:
        info = line.split()
        if info[0] in warning and info[-2][0] == '2':
            del warning[info[0]]
        elif info[-2][0] != '2' and info[0] not in warning:
            warning[info[0]] = Q.deque([datetime.strptime(info[3][1:], "%d/%b/%Y:%H:%M:%S")])
        elif info[-2][0] != '2':
            time = datetime.strptime(info[3][1:], "%d/%b/%Y:%H:%M:%S") 
            if len(warning[info[0]]) == 3 and time - warning[info[0]][-1] < timedelta(minutes = 5):
                f_out.write(line)
            elif len(warning[info[0]]) == 3 and time - warning[info[0]][-1] >= timedelta(minutes = 5):
                warning[info[0]].clear()
                warning[info[0]].append(time)
            else:
                warning[info[0]].append(time)
                while time - warning[info[0]][0] > timedelta(seconds = 20):
                    warning[info[0]].popleft()

f_out.close()
