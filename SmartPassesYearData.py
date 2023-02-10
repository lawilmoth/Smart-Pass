import csv
import re

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from datetime import datetime
from datetime import timedelta

SCHOOL_MINUTES = 7*60 #Added an hour to account for passes that end after the school day ends

filename = "SmartPasses2_2to2_8.csv"
month = 2 #Current Month
'''
filenameRegex = re.compile(r'\d+')
dateForTitle = filenameRegex.findall(filename)
print(dateForTitle)
'''

active_passes = [0]*SCHOOL_MINUTES #Iniitalizes a list with 0 passes for every minute of the day
STARTTIME = datetime(1900, 1, 1, 8, 40, 0) # Start time 8:40

#Puts times on the x axis
x_axis_list = []
month_passes = []

findDateRegex = re.compile(r'\d+')

for i in range(SCHOOL_MINUTES):
    x_axis_list.append(STARTTIME + timedelta(minutes=i))


def updateActivePasses(schoolStart:datetime, schoolEnd:int, passStart:datetime, PassEnd:datetime, activePassList:list) ->list:
    startDelta = passStart - schoolStart
    startDelta = int(startDelta.total_seconds()/60) #Delta from start of day in minutes
    passDelta = PassEnd - passStart
    passDelta = int(passDelta.total_seconds()/60) #Delta from the start of the pass to the end in minutes
    if startDelta >= 0 and startDelta + passDelta <= schoolEnd:
        for i in range(startDelta, startDelta + passDelta):
            activePassList[i]+=1

    return activePassList



with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    startTimes, durations, endTimes, months_passes = [] , [], [], []

    for row in reader:
        
        readingDate = findDateRegex.findall(row[4])
        if int(readingDate[0]) == month: #Data must be sorted by date
            try:
                passStartTime = datetime.strptime(row[5], '%I:%M%p')+timedelta(hours=2)
                duration = datetime.strptime(row[6], '%Mm%Ss')
                endTime = passStartTime + timedelta(minutes = duration.minute, seconds=duration.second)
                
                
            except:
                print(f'{duration} was an unexpected format.')
            else:
                startTimes.append(passStartTime)
                durations.append(duration)
                endTimes.append(endTime)
                active_passes = updateActivePasses(STARTTIME, SCHOOL_MINUTES, passStartTime, endTime, active_passes)
        
        else:
            month = (month - 1) % 12
            month_passes.append(active_passes)
            active_passes = [0]*SCHOOL_MINUTES

            



plt.style.use('fivethirtyeight')

fit, ax = plt.subplots()
for dataset in month_passes:
    ax.plot(dataset, active_passes, linewidth = 2)
hh_mm = DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hh_mm)

#ax.set_title(f"Passes for {dateForTitle[0]}/{dateForTitle[1]}/{dateForTitle[2]}")
ax.set_title(f"Passes for Year by Month")

ax.set_xlabel("Time of Day")
ax.set_ylabel("Active Pass Count")


plt.savefig(f"{filename[:-4]}.png", bbox_inches = 'tight')
plt.show()
print(months_passes)