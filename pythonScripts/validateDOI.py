
## text = "doi:10.1038/nphys1170"
## url = "http://dx.doi.org/10.1192/bjp.171.6.519"

fields = []

urlSplit = "http://dx.doi.org/"
IDSplit = "doi:"

file = open("ListDOI.txt","r")

for line in file:
    fields = line.split(urlSplit)
    print(fields[1])
file.close()

