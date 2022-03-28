from createMap import *
from updateData import *

if __name__ == "__main__":
    print("What do you want to do?: ")
    print("1: update map\n"
         " 2: create map")
    c = input()
    if (c == '2'):
        createMap()
    elif (c == '1'):
        UpdateSongData()
    elif (c == '3'):
        createAllMaps()