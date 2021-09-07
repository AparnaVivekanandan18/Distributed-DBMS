import json
import requests
from DBMS_Software.queryParserValidator.SelectParser import selectQueryParser
from DBMS_Software.queryProcessor.GetPath import getPath

#Creating the NODE class, that represents the Node structure in a linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

#In this LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    def insertFileToNodesSelect(self,data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    # ------------------------------------------Traversing the Linked List--------------------------------------------------
    def fetch_All_list(self):
        cur_node = self.head
        while cur_node:
            record = cur_node.data
            print("Fetched Row(s)")
            print(record)
            cur_node = cur_node.next
    #------------------------------------------Traversing the Linked List--------------------------------------------------
    def fetch_list(self,columnName,columnValue,MetaFilePath):
        ColumnNameList = []
        ColumnDataTypeList = []
        MetaDataList = []

        file = open(MetaFilePath, 'r')
        Lines = file.readlines()
        file.close()

        NumOfRecords = len(Lines)
        for eachline in Lines:
            if(NumOfRecords > 0):
                MetaDataList = eachline.split(' ')

                tempColumnName = MetaDataList[0]
                tempColumnDataType = MetaDataList[1]

                ColumnNameList.append(tempColumnName)
                ColumnDataTypeList.append(tempColumnDataType)

        cur_node = self.head
        while cur_node:
            record = cur_node.data
            self.process_record(record,columnName,columnValue,ColumnNameList,ColumnDataTypeList) #Call the function
            cur_node = cur_node.next
    #------------------------------------------Parse the Record and then do search processing--------------------------------------------------
    def process_record(self,record,columnName,columnValue,ColumnNameList,ColumnDataTypeList):
        ColumnValueList = []
        ColumnValueList = record.split('^')
        try:
            ColumnValueIndexList = []
            ColumnLength = len(ColumnValueList)
            for i in range(0,ColumnLength):
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
            for i in range (0,Length):
                if (ColumnValueIndexList[i] == ColumnNameIndex):
                    print("Fetched Row(s)")
                    print(ColumnValueList)
        except:
            return

#*--------------------------------------------Start Here----------------------------------------------*
#Instantiating the LinkedList Class
def executeSelect():

    llist_object = LinkedList()
    TableName,conditions_list,tableLocation = selectQueryParser()

    if(TableName):
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


        if (tableLocation != 'RemoteLocation'):
            #Read the Table File
            FileObject = open(TableFilePath, 'r')
            Lines = FileObject.readlines()
            FileObject.close()

            #Append the each "row of data"(record) from Student-table into seperate NODES in Linked List
            for eachline in Lines:
                row = eachline
                mod_string = row[:-1]
                llist_object.insertFileToNodesSelect(mod_string)
        #-----------------------------------------------------------------------------------------------------------------------
        if(conditions_list): # Select Condition Processing
            SearchColumnName = conditions_list[0]
            SearchColumnValue = conditions_list[1]
            if (tableLocation == 'RemoteLocation'):
                temp = {'Query': 'SELECT', 'MetaData': MetaFilePath, 'TableName': TableFilePath,'ColumnName': SearchColumnName, 'ColumnValue': SearchColumnValue}
                data = json.dumps(temp)
                url = 'http://127.0.0.1:5000/remote_end_point'
                response = requests.post(url, data=data)
                resData = (json.loads(response.text))
                return
            else:
                llist_object.fetch_list(SearchColumnName,SearchColumnValue,MetaFilePath)
        else:# Select * Processing
            if (tableLocation == 'RemoteLocation'):
                temp = {'Query': 'SELECT','MetaData': MetaFilePath, 'TableName': TableFilePath}
                data = json.dumps(temp)
                url = 'http://127.0.0.1:5000/remote_end_point'
                response = requests.post(url, data=data)
                resData = (json.loads(response.text))
                return
            else:
                llist_object.fetch_All_list()
        # -----------------------------------------------------------------------------------------------------------------------

if __name__ == "__ProcessSelectQuery__":
    executeSelect()