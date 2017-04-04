import io
from collections import defaultdict
import heapq

d = defaultdict(int)
with io.open('../log_input/log.txt', 'r', encoding='iso-8859-1') as f_in:
	for line in f_in:
		#print(re.match(regex, line).groups())
		info = line.split()
		d[info[0]] -= 1
		
h = []
for item in d:
	heapq.heappush(h, (d[item], item))

f_out = open('../log_output/hosts.txt', 'w', encoding = 'iso-8859-1')
for a, b in heapq.nsmallest(10,h):
    f_out.write(str(b) + ',' + str(-1*a) + '\n')
f_out.close()
