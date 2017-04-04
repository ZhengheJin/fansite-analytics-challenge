import io
from datetime import datetime,timedelta

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

res = sorted(list(zip(map(lambda x: -1 * x, acc), times)))

from functools import reduce

f_out = open('../log_output/hours_new.txt', 'w', encoding = 'iso-8859-1')

index = 0
busiest = []
for a, b in sorted(res):
    invalid = reduce((lambda x, y : x or y), [b - timedelta(hours = 1) < time < b + timedelta(hours = 1) for time in busiest]) if len(busiest) != 0 else False
    if invalid: continue
    busiest.append(b)
    f_out.write(str(b.strftime("%d/%b/%Y:%H:%M:%S"))+' -0400,'+str(-1*a)+'\n')
    index += 1
    if index == 10: break

f_out.close()

weekdays = [0 for i in range(7)]
hours = [0 for i in range(24)]
for i in range(len(times)):
    # sampling, considering the same time period for both weekdays and hours.
    if datetime(1995, 7, 1, 0, 0, 0) <= times[i] < datetime(1995, 7, 22, 0, 0, 0):
        weekdays[times[i].weekday()] += cnts[i]
        hours[times[i].hour] += cnts[i]

f_out = open('../log_output/visit_analysis.txt','w', encoding = 'iso-8859-1')
f_out.write("The visit analysis by weekdays:\n")
f_out.write("The average visit on Monday is %.2f%%.\n" % (100*weekdays[0]/sum(weekdays)))
f_out.write("The average visit on Tuesday is %.2f%%.\n" % (100*weekdays[1]/sum(weekdays)))
f_out.write("The average visit on Wednesday is %.2f%%.\n" % (100*weekdays[2]/sum(weekdays)))
f_out.write("The average visit on Thursday is %.2f%%.\n" % (100*weekdays[3]/sum(weekdays)))
f_out.write("The average visit on Friday is %.2f%%.\n" % (100*weekdays[4]/sum(weekdays)))
f_out.write("The average visit on Saturday is %.2f%%.\n" % (100*weekdays[5]/sum(weekdays)))
f_out.write("The average visit on Sunday is %.2f%%.\n\n" % (100*weekdays[6]/sum(weekdays)))

f_out.write("The visit analysis by hours of a day:\n")
for i in range(24):
    f_out.write("The average visit on %d:00 - %d:00 is %.2f%%.\n" % (i, i+1, 100*hours[i]/sum(hours)))
