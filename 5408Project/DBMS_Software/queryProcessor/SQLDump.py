from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import fetchFileFromGCP
import os
def createSQLDump():
    print("Enter the TableName:")
    TableName = input()
    tableLocation =  readGlobalDataDictionary(TableName)
    if(tableLocation == 'RemoteLocation'):
        fetchFileFromGCP(TableName)

    FileExtension = ".txt"
    FileName = TableName + FileExtension  # Framing the FileName
    metaFileExtension = 'MetaData.txt'
    metaDatafileName = TableName + metaFileExtension

    FileObject = open(metaDatafileName, 'r')
    Lines = FileObject.readlines()
    for eachline in Lines:
        filepath = os.path.join('E:/SQLDump_Extraction', metaDatafileName)
        if not os.path.exists('E:/SQLDump_Extraction'):
            os.makedirs('E:/SQLDump_Extraction')
        f = open(filepath, "a")
        f.write(eachline)
        f.close()
    filepath = os.path.join('E:/SQLDump_Extraction', FileName)
    if not os.path.exists('E:/SQLDump_Extraction'):
        os.makedirs('E:/SQLDump_Extraction')
    f = open(filepath, "a")

