# config
START_INDEX = 1
START_DAY_OF_WEEK = 4
DATA_TIME_FORMATE = "%Y-%m-%dT%H:%M:%S+08:00"
SAVE_NAME = "analysis.png"

# import
import csv
import matplotlib.pyplot as plt
import datetime

# read data
csvFile = open("data/occupancy.csv")
data = list(csv.reader(csvFile))

# setup plot
plt.grid(axis="both")
plt.xlabel("Time")
plt.ylabel("Number of People")

# process data
countDay = START_DAY_OF_WEEK
timeofOneWeek = []
peopleofOneWeek = []
lastTime = datetime.datetime.strptime(data[1][0], DATA_TIME_FORMATE)

for i in range(1, len(data)):
    if data[i][1] == "N/A":
        continue

    time = datetime.datetime.strptime(data[i][0], DATA_TIME_FORMATE)
    timeofOneWeek.append(time)
    peopleofOneWeek.append(int(data[i][1]))

    if lastTime.day != time.day:
        countDay += 1

    if countDay == 7:
        countDay = 1
        plt.plot(timeofOneWeek, peopleofOneWeek)
        print(timeofOneWeek)
        timeofOneWeek = []
        peopleofOneWeek = []

    lastTime = time

plt.plot(timeofOneWeek, peopleofOneWeek)

plt.savefig(SAVE_NAME)
plt.show()
