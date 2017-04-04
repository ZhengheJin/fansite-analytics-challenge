import io
from datetime import datetime,timedelta
import heapq

times = []
cnts = []
cur = None
with io.open('../log_input/log.txt', 'r', encoding='iso-8859-1') as f_in:
    for line in f_in:
        info = line.split()
        line_timestamp = datetime.strptime(info[3][1:], "%d/%b/%Y:%H:%M:%S")
        if len(times) == 0 or cur != line_timestamp:
            cur = line_timestamp
            times.append(cur)
            cnts.append(1)
        else:
            cnts[-1] += 1

acc = []
cnt = 0 # cnt accurence from times[i] to times[j]
i, j = 0,0
for i in range(len(times)):
    while j < len(times) and times[j] - times[i] < timedelta(hours = 1):
        cnt += cnts[j]
        j += 1
    acc.append(cnt)
    cnt -= cnts[i]

res = heapq.nsmallest(10, list(zip(map(lambda x: -1 * x, acc), times)))


f_out = open('../log_output/hours.txt', 'w', encoding = 'iso-8859-1')
for a, b in res:
    f_out.write(str(b.strftime("%d/%b/%Y:%H:%M:%S"))+' -0400,'+str(-1*a)+'\n')
f_out.close()
