import io
from collections import defaultdict
import heapq

from geoip import geolite2
d = defaultdict(int)
c = set()
failure = 0
success = 0
cnt = 0
with io.open('../log_input/log.txt', 'r', encoding='iso-8859-1') as f_in:
    for line in f_in:
        info = line.split()
        d[info[0]] -= 1
        cnt += 1
        match = geolite2.lookup(info[0])
        if match is not None:
            success += 1
            c.add(match.country)
print(c)
print(success, cnt)
		
