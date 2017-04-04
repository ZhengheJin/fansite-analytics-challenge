import sys
import io
from collections import defaultdict
from datetime import datetime,timedelta
import heapq
import queue as Q   # consider using collections.deque(), which requires no package installation

# count of hosts
hosts_cnt = defaultdict(int)

# count of resources bandwidth consumption
resources_cnt = defaultdict(int)

# list of identical timestamp and the number of visit per second
times = []
cnts = []

# current timestamp, used to track the timestamp
cur = None

# use of warning to track the failed login, the information stored per IP is a 
# queue of timestamp of failed login.
f_out = open(sys.argv[5], 'w', encoding = 'iso-8859-1')
warning = dict()

with io.open(sys.argv[1], 'r', encoding='iso-8859-1') as f_in:
    for line in f_in:
        info = line.split()
        line_timestamp = datetime.strptime(info[3][1:], "%d/%b/%Y:%H:%M:%S")
        
        # feature 1, store negative, better for sorting
        hosts_cnt[info[0]] -= 1

        # feature 2, store negative
        if info[-1] != '-': resources_cnt[info[6]] -= int(info[-1])
        
        # feature 3, time is non-decreasing, use list instead of dict
        if len(times) == 0 or cur != line_timestamp:
            cur = line_timestamp
            times.append(cur)
            cnts.append(1)
        else:
            cnts[-1] += 1
        
        # feature 4.
        # 1) if some IP in the warning dict has one success login, remove it from the warning
        if info[0] in warning and info[-2][0] == '2':
            del warning[info[0]]
        # 2) some IP not in the warning dict, but has one failed login
        elif info[-2][0] != '2' and info[0] not in warning:
            warning[info[0]] = Q.deque([line_timestamp])
        # 3) some IP in the warning dict, meet one more failed login
        elif info[-2][0] != '2':
            # 3.1) this IP has 3 failed login (happened in 20s, which will be guranteed later) within past 5 min, meaning
            # this IP is blocked, and such attempted should be reported.
            if len(warning[info[0]]) == 3 and line_timestamp - warning[info[0]][-1] < timedelta(minutes = 5):
                f_out.write(line)
            # 3.2) this IP has 3 failed login, but the timestamp comparing last failed login is over 5 min, meaning
            # this IP is unblocked already, thus should update the warning dict.
            elif len(warning[info[0]]) == 3 and line_timestamp - warning[info[0]][-1] >= timedelta(minutes = 5):
                warning[info[0]].clear()
                warning[info[0]].append(line_timestamp)
            # 3.3) this IP has less than 3 failed login.
            else:
                warning[info[0]].append(line_timestamp)
                # IMPORTANT: if the earlier recorded failure happens more than 20 seconds ago, compared
                # with the current failure, the earlier record should be removed.
                while line_timestamp - warning[info[0]][0] > timedelta(seconds = 20):
                    warning[info[0]].popleft()

# feature 4
f_out.close()

# the number of items we are interested to report.
interest = 10

# feature 1
# use heap, the top K item can be selected in O(n*lg(k)) time.
# use of tuple will be able to compare the occurence first, then sort by name (i.e. lexicographical order)
hosts_heap = []
for item in hosts_cnt:
    heapq.heappush(hosts_heap, (hosts_cnt[item], item))

hosts_f = open(sys.argv[2], 'w', encoding = 'iso-8859-1')
for cnt, host in heapq.nsmallest(interest, hosts_heap):
    hosts_f.write(str(host) + ',' + str(-1*cnt) + '\n')
hosts_f.close()

# feature 2
resources_heap = []
for item in resources_cnt:
    heapq.heappush(resources_heap, (resources_cnt[item], item))

resources_f = open(sys.argv[3], 'w', encoding = 'iso-8859-1')
for a, b in heapq.nsmallest(interest, resources_heap):
    resources_f.write(str(b)+'\n')
resources_f.close()

# feature 3, need to calculate the total connection within 1h.
# implemented in O(n) time
acc = [] # accumulated occurrence from time[i] to 1h later, not including time[i] + 1h.
cnt = 0 # cnt occurrence from times[i] to times[j], j not included.
i, j = 0,0
for i in range(len(times)):
    while j < len(times) and times[j] - times[i] < timedelta(hours = 1):
        cnt += cnts[j]
        j += 1
    acc.append(cnt)
    cnt -= cnts[i]

# map applies (-1)* to each count, zip convert two list into one list of tuple
res = heapq.nsmallest(interest, list(zip(map(lambda x: -1 * x, acc), times)))

f_out = open(sys.argv[4], 'w', encoding = 'iso-8859-1')
for a, b in res:
    f_out.write(str(b.strftime("%d/%b/%Y:%H:%M:%S"))+' -0400,'+str(-1*a)+'\n')
f_out.close()
