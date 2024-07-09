import datetime
import random
import time

def main():
    # We save the dat in an xml file to plot it
    file = open("ListAccessTiming.xml", "w")

    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')

    file.write('<Plot title="Average List Element Access Time"')

    # Two test lists with 1000 and 2000000 elements
    xmin = 1000
    xmax = 2000000

    # Record the list sizes in xList and the average access time within
    # a list that size in yList for 1000 retrievals
    xList = []
    yList = []
    for x in range(xmin, xmax+1, 1000):
        xList.append(x)

        prod = 0

        # creates a list of size x with all 0's
        lst = [0] * x

        # Garbage collection happens in this sleep
        time.sleep(1)

        starttime = datetime.datetime.now()

        for v in range(1000):
            # Find a random location within the list
            # retrive value, do a dummy op to check it is there
            index = random.randint(0, x-1)
            val = lst[index]
            prod = prod * val

        # time after the 1000 test retrievals
        endtime = datetime.datetime.now()