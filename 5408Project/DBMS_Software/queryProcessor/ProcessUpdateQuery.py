import json
import requests

from DBMS_Software.queryParserValidator.UpdateParser import updateQueryParser
from DBMS_Software.queryProcessor.GetPath import getPath
from DBMS_Software.queryProcessor.GetFiles import getEventLogPath
from datetime import datetime

class Node:
    # Constructor to initialize the node object
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked List Class
class LinkedList2:
    def __init__(self):
        self.head = None

    # ----------------------------------------Insering the Records to the Linked List-------------------------------------------------
    def insertFileToNodesUpdate(self, data):
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

    # -----------------------------------Updating the nodes in linked list---------------------------------------------------
    def updateNodesInList(self, updateColumnName, updateColumnValue, updateConditionColumnName,
                          updateConditionColumnValue, metaDatafileName):
        ColumnNameList = []
        ColumnDataTypeList = []
        MetaDataList = []

        metaDatafileName = metaDatafileName  # Framing the FileName
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
        recordUpdateCount = 0
        while trav_node:
            record = trav_node.data
            new_record = self.nodesToBeUpdated(record, updateColumnName, updateColumnValue, updateConditionColumnName,
                                               updateConditionColumnValue, ColumnNameList,
                                               ColumnDataTypeList)  # Call the Function

            if (new_record != record):
                trav_node.data = new_record
                trav_node = trav_node.next
                recordUpdateCount += 1

            else:
                trav_node = trav_node.next
        return recordUpdateCount

    # -----------------------------------finding whether the selected node needs to be updated----------------------------------------------------
    def nodesToBeUpdated(self, record, columnName, columnValue, ColumnConditionName, ColumnConditionValue,
                         ColumnNameList, ColumnDataTypeList):
        ColumnValueList = []
        ColumnValueList = record.split('^')
        ColumnNameIndex = ""

        try:
            ColumnNameIndex = ColumnNameList.index(columnName)
        except:
            print("Not Found")
            return

        try:
            ColumnLength = len(ColumnValueList)
            for i in range(0, ColumnLength):
                if (ColumnValueList[i] == ColumnConditionValue):
                    ColumnValueList[ColumnNameIndex] = columnValue;
                    break;
            ColumnValueListNew = '^'.join(ColumnValueList)
            return ColumnValueListNew
        except:
            return ColumnValueList


# ----------------------------------------------------------------------------------------------------------------------
def writeEventLog(FileName):
    Event = 'UPDATE'
    DateTime = str(datetime.now())
    DateTime = "".join(DateTime.split())

    EventLogFile = "EventLog.txt"
    path = getEventLogPath()
    LogFilePath = path + EventLogFile

    EventLogFile = open(LogFilePath, 'a+')
    EventLogFile.write(FileName + ' ' + Event + ' ' + DateTime + "\n")
    EventLogFile.close()


# -----------------------------------Starts Here---------------------------------------------------------------------
def executeUpdate():
    llist_object = LinkedList2()

    conditions_list = []
    column_list = []
    TableName, column_list, conditions_list, tableLocation = updateQueryParser()

    if (TableName):
        updateColumnName = column_list[0]
        updateColumnValue = column_list[1]

        updateConditionColumnName = conditions_list[0]
        updateConditionColumnValue = conditions_list[1]

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
                llist_object.insertFileToNodesUpdate(mod_string)

        if (tableLocation == 'RemoteLocation'):
            temp = {'Query': 'UPDATE','MetaData':MetaFilePath,'TableName':TableFilePath,'ColumnName':updateColumnName,'ColumnValue':updateColumnValue,'ConditionColumnName':updateConditionColumnName,'ConditionColumnValue':updateConditionColumnValue}
            data = json.dumps(temp)
            url = 'http://127.0.0.1:5000/remote_end_point'
            response = requests.post(url, data=data)
            resData = (json.loads(response.text))
            return
        else:
            recordUpdateCount = llist_object.updateNodesInList(updateColumnName,updateColumnValue,updateConditionColumnName,updateConditionColumnValue,MetaFilePath)

        # Writing each nodes to the text file again.
        if (recordUpdateCount > 0):
            llist_object.writeNodesToFile(TableFilePath)
            writeEventLog(TableName)


if __name__ == "__ProcessUpdateQuery__":
    executeUpdate()