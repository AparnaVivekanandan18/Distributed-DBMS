from DBMS_Software.queryProcessor.GetFiles import getGDDFile
#-------------------------------------Reading the Location in Global Data Dictionary-----------------------------------------------
def readGlobalDataDictionary(TableName):

    FileName = "GlobalDataDictionaryFile.txt"
    Path = getGDDFile()
    FilePath = Path+FileName

    FileObject = open(FilePath, 'r')
    Lines = FileObject.readlines()
    for eachline in Lines:
         split = eachline.split(' ')
         table = split[0]
         if (table == TableName):
            location = split[1]
            tableLocation = location[:-1]
            return tableLocation
