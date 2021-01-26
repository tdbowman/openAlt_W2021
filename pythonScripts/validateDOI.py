
text = "doi:10.1038/nphys1170"
url = "http://dx.doi.org/10.1192/bjp.171.6.519"
spl = "http://dx.doi.org/"

newText = text.split(':')
urlText = url.split(spl)

x = newText[1]
y = urlText[1]

print(y)
