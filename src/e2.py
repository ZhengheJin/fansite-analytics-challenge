import io,sys
from collections import defaultdict
d = defaultdict(int)
with io.open(sys.argv[1], 'r', encoding='iso-8859-1') as f_in:
    for line in f_in:
        info = line.split()
        if info[-2][0] != '2':
            d[info[0]] -= 1
		
import heapq
h = []
for item in d:
    heapq.heappush(h, (d[item], item))

f_out = open(sys.argv[2], 'w', encoding = 'iso-8859-1')
for a, b in heapq.nsmallest(10,h):
    f_out.write(str(b)+'\n')
    #f_out.write(str(b)+','+str(-1*a)+'\n')
f_out.close()
