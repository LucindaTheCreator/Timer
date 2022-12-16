import time


def calcTimescore(hh,mm,ss):
    return hh*3600+mm*60+ss

def getLocTimeGreet():
    time_now = time.asctime()
    times = list(map(int,time_now.split()[-2].split(":")))
    key = calcTimescore(times[0],times[1],times[2])//14440
    dates = {0:"Good midnight,", 1:"Good morning,", 2:"Good late morning!,", 3:"Good afternoon,",
             4:"Good evening,", 5:"Good night,"}
    return dates.get(key,"Hi,")

