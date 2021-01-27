
## text = "doi:10.1038/nphys1170"
## url = "http://dx.doi.org/10.1192/bjp.171.6.519"

fields = []
IDSplit = "doi:"
urlSplit = "http://dx.doi.org/"

file = open("ListDOI.txt","r")

for line in file:
    ##fields = line.split(IDSplit)

    if(file.read(4) == "doi:"):
        fields = line.split(IDSplit)
    elif(file.read(18) == "http://dx.doi.org/"):
        fields = line.split(urlSplit)
    elif(file.read(3) == "10."):
        fields = line
    else:
        print("Error retrieving DOI.")

    try:
        from crossref.restful import Works
        works = Works()

        # Request data from the crossref API, save json as x
        x = works.doi(fields[1])
        if (x['author']):
            authorList = x['author']
            for index, authorDetail in enumerate(authorList):
                first_name = authorDetail['given']
                last_name = authorDetail['family']
                print(first_name + ' ' + last_name)
                
    except ImportError:
        print("You need to install the crossref api with 'pip install crossrefapi' first")
    except:
        print("Unspecified error")

file.close()


