import csv
import pandas

### Start of Darpan's Work ###

#array of DOIs
doi_arr = []

#directory of doi list
dir = 'C:\\Users\\darpa\\Desktop\\openAlt_W2021\\pythonScripts\\template_doi.csv'



#pandas library reads doi list
doi_list = pandas.read_csv(dir)


#adds doi values into array and prints the array
for x in range(len(doi_list)):
    doi_arr.append(doi_list.values[x][0])


print(doi_arr)

## End of Darpan's Work
