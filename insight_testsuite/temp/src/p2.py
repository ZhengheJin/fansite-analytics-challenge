import io
from collections import defaultdict
d = defaultdict(int)
with io.open('../log_input/log.txt', 'r', encoding='iso-8859-1') as f_in:
	for line in f_in:
		#print(re.match(regex, line).groups())
		info = line.split()
		if info[-1] == '-': continue
		#if info[5] != '"GET' or info[5] != '"POST': print(info[5])
		#print(info)
		d[info[6]] -= int(info[-1])
		
import heapq
h = []
for item in d:
	heapq.heappush(h, (d[item], item))

f_out = open('../log_output/resources.txt', 'w', encoding = 'iso-8859-1')
for a, b in heapq.nsmallest(10,h):
    f_out.write(str(b)+'\n')
f_out.close()
