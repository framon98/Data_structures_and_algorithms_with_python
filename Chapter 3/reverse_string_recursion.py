#!/usr/bin/python3

def revString(str_seq):
    if str_seq == "":
        return ""
    
    restrev = revString(str_seq[1:])
    first = str_seq[0:1]

    result = restrev + first

    return result

def main():

    print(revString("hello"))

if __name__ == "__main__":
    main()