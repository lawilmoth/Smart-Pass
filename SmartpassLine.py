import csv
import re

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from datetime import datetime
from datetime import timedelta

SCHOOL_MINUTES = 7*60 #Added an hour to account for passes that end after the school day ends

filename = "SmartpassYearto2_9.csv"


filenameRegex = re.compile(r'\d+')
dateForTitle = filenameRegex.findall(filename)



title = f"Passes for {dateForTitle[0]}/{dateForTitle[1]}/{dateForTitle[2]}"
#The file naming system worked when the file name is dd_mm_yy.csv


active_passes = [0]*SCHOOL_MINUTES #Iniitalizes a list with 0 passes for every minute of the day
STARTTIME = datetime(1900, 1, 1, 8, 40, 0) # Start time 8:40


#Pupts times on the x axis
x_axis_list = []
for i in range(SCHOOL_MINUTES):
    x_axis_list.append(STARTTIME + timedelta(minutes=i))


def updateActivePasses(schoolStart:datetime, schoolEnd:int, passStart:datetime, PassEnd:datetime, activePassList:list) ->list:
    '''Updates the number of  students in the hall with each new line of the csv'''
    startDelta = passStart - schoolStart
    startDelta = int(startDelta.total_seconds()/60) #Delta from start of day in minutes
    passDelta = PassEnd - passStart
    passDelta = int(passDelta.total_seconds()/60) #Delta from the start of the pass to the end in minutes
    if startDelta >= 0 and startDelta + passDelta <= schoolEnd:
        for i in range(startDelta, startDelta + passDelta):
            activePassList[i]+=1

    return activePassList



with open(filename) as f:
    '''Open file and update data in for start time, end time, and active passes'''
    reader = csv.reader(f)
    header_row = next(reader)

    startTimes, durations, endTimes = [] , [], []

    for row in reader:
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
            updateActivePasses(STARTTIME, SCHOOL_MINUTES, passStartTime, endTime, active_passes)
            
            



plt.style.use('fivethirtyeight')

fit, ax = plt.subplots()


ax.plot(x_axis_list, active_passes, linewidth = 2)
hh_mm = DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hh_mm)



ax.set_title(title)

ax.set_xlabel("Time of Day")
ax.set_ylabel("Active Pass Count")


plt.savefig(f"{filename[:-4]}.png", bbox_inches = 'tight')
