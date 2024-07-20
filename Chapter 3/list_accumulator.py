#!/usr/bin/python3
def revList(lst):
    """
    This function uses the accumulator pattern
    to reverse the list. This is not as efficient
    as using a recusrive approach. This uses more
    cpu cycles since it has to read the whole list
    and add it to a new copy
    """
    accumulator = []

    for idx in lst:
        accumulator = [idx] + accumulator

    return accumulator
    
def main():
    print(revList([1,2,3,4]))

if __name__ == "__main__":
    main()