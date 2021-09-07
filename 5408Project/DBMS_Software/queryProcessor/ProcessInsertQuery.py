from datetime import datetime
from DBMS_Software.queryParserValidator.InsertParser import validateInsertStatement
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary, fetchFileFromGCP


def executeInsert():

    TableName,data_list, = validateInsertStatement()

    if(TableName!=''):
        opentable = open(TableName+".txt", "a+")
        count=0;
        for i in data_list:
            count +=1
            if(count==len(data_list)):
                opentable.write(i)
            else:
                opentable.write(i + "^")
        opentable.write("\n")
        print("SUCCESS: Data inserted successfully..")
        writeLogFiles(TableName)

def writeLogFiles(tableName):
    TableName = tableName

    FileName = "GeneralLog.txt"
    FileObject = open(FileName, 'r+')
    Lines = FileObject.readlines()
    eachlinelist = []
    for eachline in Lines:
        eachlinelist.append(eachline)

    FileObject.truncate(0)
    FileObject.close()
    for i in eachlinelist:
        GeneralLogList = i.split(' ')
        fetchedtablename = GeneralLogList[0]
        UpdateFile = open(FileName, 'a+')
        if (fetchedtablename == TableName):
            counter = int(GeneralLogList[1]) + 1
            UpdateFile.write(GeneralLogList[0] + " " + str(counter) + " " + GeneralLogList[2])
        else:
            UpdateFile.write(GeneralLogList[0] + " " + GeneralLogList[1] + " " + GeneralLogList[2])

    Event = 'INSERT'
    DateTime = str(datetime.now())
    DateTime = "".join(DateTime.split())
    EventLogFile = "EventLog.txt"
    EventLogFile = open(EventLogFile, 'a+')
    EventLogFile.write(TableName + ' ' + Event + ' ' + DateTime + "\n")
    EventLogFile.close()


