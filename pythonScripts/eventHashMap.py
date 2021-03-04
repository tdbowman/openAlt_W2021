
def eventHashMap():
    eventDict = {"123":None, "234":None, "567":None}
    print(type(eventDict))

    for key in eventDict:
        if (key == "123"):
            print(eventDict[key])

  
if __name__ == '__main__':
    eventHashMap()