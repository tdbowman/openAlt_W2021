import configparser
import os

#Author: Mohammad Tahmid 
#Lines: 1-111
#Descrption: Creation of config script to create/recreate it if needed

#Creation and insertion of config file information
#-----------------------------------------------------------------------
config = configparser.ConfigParser()

#Creation of configuration information for the DOI database
config['doidata'] = {}
configDOI = config['doidata']
configDOI['database'] = 'doidata'
configDOI['username'] = 'root'
configDOI['password'] = ''
configDOI['host'] = '127.0.0.1'

#Creation of configuration information for the DOI event data
config['crossrefeventdatamain'] = {}
configDOI = config['crossrefeventdatamain']
configDOI['database'] = 'crossrefeventdatamain'
configDOI['username'] = 'root'
configDOI['password'] = ''
configDOI['host'] = '127.0.0.1'

#Creation of configuration information for the DOI OpenCitations data
config['opencitations'] = {}
configDOI = config['opencitations']
configDOI['database'] = 'opencitations'
configDOI['username'] = 'root'
configDOI['password'] = ''
configDOI['host'] = '127.0.0.1'

#Creation of configuration information for Event data API
config['Crossref Event API'] = {}
configDOI = config['Crossref Event API']
configDOI['link'] = 'https://api.eventdata.crossref.org/v1/events?mailto=GroovyBib@example.org&obj-id='

#Creation of configuration information for Metadata API
config['Crossref Metadata API'] = {}
configDOI = config['Crossref Metadata API']
configDOI['link'] = 'https://api.crossref.org/works/'

#Creation of configuration information of the link for Opencitations Citation API
config['OpenCitations Citation API'] = {}
configDOI = config['OpenCitations Citation API']
configDOI['link'] = 'https://w3id.org/oc/index/coci/api/v1/citations/'

#Creation of configuration information of the link for Opencitations Reference API
config['OpenCitations Reference API'] = {}
configDOI = config['OpenCitations Reference API']
configDOI['link'] = 'https://w3id.org/oc/index/coci/api/v1/references/'

#Creation of configuration information of the link for Opencitations Citation Count API
config['OpenCitations Citation Count API'] = {}
configDOI = config['OpenCitations Citation Count API']
configDOI['link'] = 'https://w3id.org/oc/index/coci/api/v1/citation-count/'

#Creation of configuration information of the link for Opencitations Reference Count API
config['OpenCitations Reference Count API'] = {}
configDOI = config['OpenCitations Reference Count API']
configDOI['link'] = 'https://w3id.org/oc/index/coci/api/v1/reference-count/'


#File path for the location of the configuration file in the database
configFileName = "openAltConfig.ini"
filePath = os.path.dirname(os.path.realpath(__file__))
filePath = os.path.join(filePath, configFileName)

with open(filePath, 'a+') as configfile:
    config.write(configfile)

configfile.close()


#Reading in file information
#-----------------------------------------------------------------------

'''
#Creation of configparser object
config = configparser.ConfigParser()
config.sections()
print(config.sections())

#Find and reads the config file
#IMPORTANT: Please change "dirNum" to the number of directories that need to be traveled up from the direcotry of the file you are working in to find the config file
a = os.path.dirname(os.path.abspath(__file__))
print(a)

dirNum = 0

for i in range(dirNum):
	a= os.path.dirname(a)
	print(a)

filePath = os.path.join(a, dataDirectory)

config.read(filePath)
#END OF IMPORTANT

b = config['doidata']['username']
print(b)

exampleValue = config['opencitations']['username']
print(exampleValue)

configOC = config['OpenCitations Citation API']
print(configOC['link'])
'''