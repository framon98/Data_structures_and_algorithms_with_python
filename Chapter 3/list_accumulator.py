#!/usr/bin/python3
def revList(lst):
    accumulator = []

    for idx in lst:
        accumulator = [idx] + accumulator

    return accumulator
    
def main():
    print(revList([1,2,3,4]))

if __name__ == "__main__":
    main()