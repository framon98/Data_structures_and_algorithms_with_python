#!/usr/bin/python3
import time

def SumFirstN(n):
    return n * (n+1) //2

def main():
    x = int(input("Please enter a non-negative integer: "))

    starttime = time.process_time_ns()
    s = SumFirstN(x)
    endtime = time.process_time_ns()

    deltaT = endtime - starttime
    print(f"It took {deltaT} seconds")

    print(f"The sum of the first {x} integers is {s}.")

if __name__ == "__main__":
    
    main()
