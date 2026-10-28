# config
START_INDEX = 1
START_DAY_OF_WEEK = 4
DATA_TIME_FORMATE = "%Y-%m-%dT%H:%M:%S+08:00"
SAVE_NAME = "analysis.png"
THRESHOLD = 40

# import
import csv
import matplotlib.pyplot as plt
import datetime

# read data
csvFile = open("data/occupancy.csv")
data = list(csv.reader(csvFile))

# setup plot
plt.figure(figsize=(40, 8))
plt.grid(axis="both")
plt.xlabel("Time")
plt.ylabel("Number of People")

# process data
countDay = START_DAY_OF_WEEK
timeofOneWeek = []
peopleofOneWeek = []
lastTime = datetime.datetime.strptime(data[START_INDEX][0], DATA_TIME_FORMATE)

# plot threshold
time = datetime.datetime.strptime("2026-10-11T09:10:00+08:00", DATA_TIME_FORMATE)
while time <= datetime.datetime.strptime(
    "2026-10-17T20:40:00+08:00", DATA_TIME_FORMATE
):
    if time.hour >= 9 and time.hour < 21:
        timeofOneWeek.append(time.strftime("%a %H:%M"))
        peopleofOneWeek.append(THRESHOLD)

    time += datetime.timedelta(minutes=30)
plt.plot(timeofOneWeek, peopleofOneWeek)

# plot real data
timeofOneWeek = []
peopleofOneWeek = []
for i in range(START_INDEX, len(data)):
    time = datetime.datetime.strptime(data[i][0], DATA_TIME_FORMATE)

    if lastTime.day != time.day:
        countDay += 1
        plt.plot(timeofOneWeek, peopleofOneWeek)
        timeofOneWeek = []
        peopleofOneWeek = []

    if countDay > 7:
        countDay = 1
        # plt.plot(timeofOneWeek, peopleofOneWeek)
        # timeofOneWeek = []
        # peopleofOneWeek = []

    if data[i][1] == "N/A":
        continue

    lastTime = time

    timeofOneWeek.append(time.strftime("%a %H:%M"))
    peopleofOneWeek.append(int(data[i][1]))

plt.plot(timeofOneWeek, peopleofOneWeek)
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.savefig(SAVE_NAME)
# plt.show()
