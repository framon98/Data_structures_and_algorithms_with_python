#!/usr/bin/python3

def revList2(lst):
    def revListHelper(index):
        if index == -1:
            return []
        
        restrev = revListHelper(index - 1)
        first = [lst[index]]

        # Now put them together
        result = first + restrev

        return result
    
    #This is the only line for the revList2 
    return revListHelper(len(lst) - 1)

def main():
    print(revList2([1, 2, 3, 4]))

if __name__ == "__main__":
    main()