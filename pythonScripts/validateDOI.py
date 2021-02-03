import re 

mylines = []
with open ('ListDOI.txt', 'rt') as myfile:
    for myline in myfile:
        mylines.append(myline)
# print(mylines)

str = "doi:"
url = "http://dx.doi.org/"
character = "10."

for index in mylines:
    if  index.find(str) != -1:
        search = index.split(str)
        print("Found doi " + search[1])
    elif index.find(url) != -1:
        search = index.split(url)
        print("Found url " + search[1])
    elif index.find(character) != -1:
        search = index.split(character)
        print("Found pattern " + search[1])
    else:
        print("Not Found.\n")

    try:
        from crossref.restful import Works
        works = Works()

        # Request data from the crossref API, save json as x
        x = works.doi(search[1])
        if (x['author']):
            authorList = x['author']
            for index, authorDetail in enumerate(authorList):
                first_name = authorDetail['given']
                last_name = authorDetail['family']
                print(first_name + ' ' + last_name + "\n")
                
    except ImportError:
        print("You need to install the crossref api with 'pip install crossrefapi' first\n")
    except:
        print("Unspecified error\n")
    