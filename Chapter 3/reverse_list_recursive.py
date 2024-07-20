#!/usr/bin/python3

def revList(lst):
    # Base case
    if lst == []:
        return []
    
    # This is the recursive part. It works beacuase we 
    # called it on something smaller. 
    restrev = revList(lst[1:])
    first = lst[0:1]

    # ADd the first to the rest of the list
    result= restrev + first

    return result

def main():
    print(revList([1, 2, 3, 4]))


if __name__ == "__main__":
    main()