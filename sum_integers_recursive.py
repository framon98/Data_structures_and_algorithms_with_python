#!/usr/bin/python3
import time

def recSumFirstN(n):
    if n ==0:
        return 0
    else:
        return recSumFirstN(n-1) + n
    
def main():
    x = int(input("Please enter a non-negative integer: "))

    starttime = time.process_time_ns()
    s = recSumFirstN(x)
    endtime = time.process_time_ns()

    deltaT = endtime - starttime
    print(f"It took {deltaT} seconds")

    print(f"The sum of the first {x} integers is {s}.")


if __name__ == "__main__":
    main()