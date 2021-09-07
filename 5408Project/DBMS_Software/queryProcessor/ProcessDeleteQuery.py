import json
import requests

from DBMS_Software.queryParserValidator.DeleteParser import deleteQueryParser
from DBMS_Software.queryProcessor.GetPath import getPath
from DBMS_Software.queryProcessor.GetFiles import getEventLogPath
from DBMS_Software.queryProcessor.GetFiles import getGeneralLogPath

import os

from datetime import datetime
# Node class
class Node:
    # Constructor to initialize the node object
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked List Class
class LinkedList1:
    def __init__(self):
        self.head = None

    #----------------------------------------Insering the Records to the Linked List-------------------------------------------------
    def insertFileToNodesDelete(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    # ---------------------------------------Writing the Linked List into the text file----------------------------------------------
    def writeNodesToFile(self, FileName):
        cur_node = self.head
        f = open(FileName, "r+")
        f.truncate(0)
        while cur_node:
            record = cur_node.data
            f = open(FileName, "a+")
            f.write(record + "\n")
            f.close()
            cur_node = cur_node.next

    # -----------------------------------Deleting the nodes in linked list---------------------------------------------------
    def deleteNodesFromList(self, deleteColumnName, deleteColumnValue,metaDatafileName):
        ColumnNameList = []
        ColumnDataTypeList = []
        MetaDataList = []

        metaDatafileName = metaDatafileName # Framing the FileName
        file = open(metaDatafileName, 'r')
        Lines = file.readlines()
        file.close()

        NumOfRecords = len(Lines)
        for eachline in Lines:
            if (NumOfRecords > 0):
                MetaDataList = eachline.split(' ')

                tempColumnName = MetaDataList[0]
                tempColumnDataType = MetaDataList[1]

                ColumnNameList.append(tempColumnName)
                ColumnDataTypeList.append(tempColumnDataType)

        trav_node = self.head
        prev_node = self.head
        recordDeletedCount = 0
        while trav_node:
            record = trav_node.data
            canBeDeleted = 0
            canBeDeleted = self.nodesToBeDeleted(record, deleteColumnName, deleteColumnValue, ColumnNameList,ColumnDataTypeList)
            if (canBeDeleted == 1):
                if (self.head == trav_node):
                    trav_node = trav_node.next
                    prev_node = trav_node.next
                    self.head = trav_node
                    recordDeletedCount += 1
                elif (self.head != trav_node and trav_node.next != None):
                    prev_node.next = trav_node.next
                    trav_node = trav_node.next
                    recordDeletedCount += 1
                else:
                    prev_node.next = trav_node.next
                    trav_node = None
                    prev_node = None
                    recordDeletedCount += 1
                    break
            else:
                prev_node = trav_node
                trav_node = trav_node.next
        return recordDeletedCount
    # -----------------------------------finding whether the selected node needs to be deleted----------------------------------------------------
    def nodesToBeDeleted(self, record, columnName, columnValue, ColumnNameList, ColumnDataTypeList):
        ColumnValueList = []
        ColumnValueList = record.split('^')
        try:
            ColumnValueIndexList = []
            ColumnLength = len(ColumnValueList)
            for i in range(0, ColumnLength):
                if (ColumnValueList[i] == columnValue):
                    ColumnValueIndexList.append(i)
        except:
            return

        try:
            ColumnNameIndex = ColumnNameList.index(columnName)
        except:
            print("ColumnName Not Found")
            return

        try:
            Length = len(ColumnValueIndexList)
            for i in range(0, Length):
                if (ColumnValueIndexList[i] == ColumnNameIndex):
                    canBeDeleted = 1
                    return canBeDeleted
        except:
            return
# -----------------------------------Updating the General Log---------------------------------------------------------------------
def writeLogFile(tableName,recordDeletedCount):
    TableName = tableName

    FileName = "GeneralLog.txt"
    path = getGeneralLogPath()
    LogFilePath = path + FileName

    FileObject = open(LogFilePath, 'r+')
    Lines = FileObject.readlines()
    eachlinelist = []
    for eachline in Lines:
        eachlinelist.append(eachline)

    FileObject.truncate(0)
    FileObject.close()
    for i in eachlinelist:
        GeneralLogList = i.split(' ')
        fetchedtablename = GeneralLogList[0]
        UpdateFile = open(LogFilePath, 'a+')
        if (fetchedtablename == TableName):
            counter = int(GeneralLogList[1]) - recordDeletedCount
            UpdateFile.write(GeneralLogList[0] + " " + str(counter) + " " + GeneralLogList[2])
        else:
            UpdateFile.write(GeneralLogList[0] + " " + GeneralLogList[1] + " " + GeneralLogList[2])

# -----------------------------------Updating the Event Log---------------------------------------------------------------------
def writeEventLog(FileName):
    Event = 'DELETE'
    DateTime = str(datetime.now())
    DateTime = "".join(DateTime.split())

    EventLogFile = "EventLog.txt"
    path = getEventLogPath()
    LogFilePath = path + EventLogFile

    EventLogFile = open(LogFilePath, 'a+')
    EventLogFile.write(FileName + ' ' + Event + ' ' + DateTime + "\n")
    EventLogFile.close()
#*---------------------------------------------Execution Begins Here----------------------------------------------------------------
def executeDelete():
    llist_object = LinkedList1()
    conditions_list = []
    TableName,conditions_list,tableLocation = deleteQueryParser()

    if (TableName):
        deleteColumnName = conditions_list[0]
        deleteColumnValue = conditions_list[1]

        # Getting MetaDataFile of the Table
        metaFileExtension = 'Metadata.txt'
        metaDatafileName = TableName + metaFileExtension
        if (tableLocation == 'RemoteLocation'):
            MetaFilePath = metaDatafileName
        else:
            Path = getPath()
            MetaFilePath = Path + metaDatafileName

        # Getting File of the Table
        FileExtension = ".txt"
        FileName = TableName + FileExtension  # Framing the FileName
        if (tableLocation == 'RemoteLocation'):
            TableFilePath = FileName
        else:
            Path = getPath()
            TableFilePath = Path + FileName

        # Reading the text file
        if (tableLocation != 'RemoteLocation'):
            FileObject = open(TableFilePath, 'r')
            Lines = FileObject.readlines()
            FileObject.close()

            # Insert each "row of data"(record) from Student-table text file into seperate NODES in Linked List
            for eachline in Lines:
                row = eachline
                mod_string = row[:-1]
                llist_object.insertFileToNodesDelete(mod_string)

        if (tableLocation == 'RemoteLocation'):
            temp = {'Query': 'DELETE','MetaData':MetaFilePath,'TableName':TableFilePath,'ColumnName':deleteColumnName,'ColumnValue':deleteColumnValue}
            data = json.dumps(temp)
            url = 'http://127.0.0.1:5000/remote_end_point'
            response = requests.post(url, data=data)
            resData = (json.loads(response.text))
            return
        else:
            recordDeletedCount = llist_object.deleteNodesFromList(deleteColumnName,deleteColumnValue,MetaFilePath)

        # Writing each nodes to the text file again.
        if(recordDeletedCount > 0):
            llist_object.writeNodesToFile(TableFilePath)
            writeLogFile(TableName,recordDeletedCount)
            writeEventLog(TableName)


if __name__ == "__ProcessDeleteQuery__":
    executeDelete()