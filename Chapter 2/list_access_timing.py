import datetime
import random
import time

def main():
    # We save the dat in an xml file to plot it
    file = open("ListAccessTiming.xml", "w")

    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')

    file.write('<Plot title="Average List Element Access Time">\n')

    # Two test lists with 1000 and 2000000 elements
    xmin = 1000
    xmax = 200000

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

        deltaT = endtime - starttime

        # Divide by 1000 for the average access time
        # But also multiply by 1000000 for microseconds
        accessTime = deltaT.total_seconds() * 1000

        yList.append(accessTime)

    file.write('    <Axes>\n')
    file.write('        <XAxis min="'+str(xmin)+'" max="'+str(xmax)+'">List Size</XAxis>\n')
    file.write('        <YAxis min="'+str(min(yList))+'" max="'+str(60)+'">Microseconds</YAxis>\n')
    file.write('    </Axes>\n')

    file.write('    <Sequence title="Average ACcess Time vs List Size" color="red">\n')

    for idxi in range(len(xList)):
        file.write('    <DataPoint x="'+str(xList[idxi])+'" y="'+str(yList[idxi])+'"/>\n')

    file.write('    </Sequence>')

    # This part of the program tests access at 100 random locations within a list 
    # of a 200000 elements to measure same amoutn fo time for any position
    xList = lst
    yList = [0] * 200000

    time.sleep(2)

    for idxi in range(100):
        starttime = datetime.datetime.now()
        index = random.randint(0, 200000-1)
        xList[index] = xList[index] + 1
        endtime = datetime.datetime.now()
        deltaT = endtime - starttime
        yList[index] = yList[index] + deltaT.total_seconds() * 1000000

    file.write('    <Sequence title="Access Time Distribution" color="blue"')

    for idxi in range(len(xList)):
        if xList[idxi] > 0:
            file.write('    <DataPoint x="'+str(idxi)+'" y="'+str(yList[idxi]/xList[idxi])+'"/>\n')

    file.write('    </Sequence>\n')
    file.write('</Plot>\n')
    file.close()

if __name__ == "__main__":
    main()