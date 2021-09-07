import os
from flask import Flask, request
import json

from DBMS_Software.queryProcessor.ProcessDeleteQuery import LinkedList1,writeLogFile, writeEventLog
from DBMS_Software.queryProcessor.ProcessUpdateQuery import LinkedList2, writeEventLog
from DBMS_Software.queryProcessor.ProcessSelectQuery import LinkedList

app = Flask(__name__)

@app.route("/")
def test():
    return "Hellow World"

@app.route("/remote_end_point", methods=["POST"])
def remote_end_point():
    data = request.data
    if not data:
        return (
            "Invalid Request",
            400,
        )
    input = data.decode('utf-8')
    input = json.loads(input)
    output = ""

    # extract the details from dictionary
    KeyValueList = []
    for key in input:
        wordKey = key.strip()
        Values =  input[wordKey]
        KeyValueList.append(Values)

    QueryOperator = KeyValueList[0]
    MetaData = KeyValueList[1]
    Tablename = KeyValueList[2]

    dir = os.path.dirname(os.path.abspath(__file__))
    MetaData = dir + '/DBMS_Software/Database/' + MetaData
    Tablename = dir + '/DBMS_Software/Database/' + Tablename


    #--------------------DELETE OPERATION-----------------------------------------------------------
    if (QueryOperator == 'DELETE'):
        llist_object = LinkedList1()
        ColumnName = KeyValueList[3]
        ColumnValue = KeyValueList[4]
        FileObject = open(Tablename, 'r')
        Lines = FileObject.readlines()
        FileObject.close()

        # Insert each "row of data"(record) from Student-table text file into seperate NODES in Linked List
        for eachline in Lines:
            row = eachline
            mod_string = row[:-1]
            llist_object.insertFileToNodesDelete(mod_string)

        recordCount = llist_object.deleteNodesFromList(ColumnName,ColumnValue,MetaData)

        # Writing each nodes to the text file again.
        if (recordCount > 0):
            llist_object.writeNodesToFile(Tablename)
            writeLogFile(Tablename, recordCount)
            writeEventLog(Tablename)

        return str(recordCount)

    # --------------------UPDATE OPERATION-----------------------------------------------------------
    if (QueryOperator == 'UPDATE'):
        llist_object = LinkedList2()
        ColumnName = KeyValueList[3]
        ColumnValue = KeyValueList[4]
        ColumnConditionName = KeyValueList[5]
        ColumnConditionValue = KeyValueList[6]

        FileObject = open(Tablename, 'r')
        Lines = FileObject.readlines()
        FileObject.close()

        # Insert each "row of data"(record) from Student-table text file into seperate NODES in Linked List
        for eachline in Lines:
            row = eachline
            mod_string = row[:-1]
            llist_object.insertFileToNodesUpdate(mod_string)

        recordCount = llist_object.updateNodesInList(ColumnName,ColumnValue,ColumnConditionName,ColumnConditionValue,MetaData)

        # Writing each nodes to the text file again.
        if (recordCount > 0):
            llist_object.writeNodesToFile(Tablename)
            writeEventLog(Tablename)

        return str(recordCount)
    # --------------------SELECT OPERATION-----------------------------------------------------------
    if (QueryOperator == 'SELECT'):
        llist_object = LinkedList()
        recordCount = 0
        FileObject = open(Tablename, 'r')
        Lines = FileObject.readlines()
        FileObject.close()

        # Insert each "row of data"(record) from Student-table text file into seperate NODES in Linked List
        for eachline in Lines:
            row = eachline
            mod_string = row[:-1]
            llist_object.insertFileToNodesSelect(mod_string)

        KeyValueListLength = len(KeyValueList)
        if (KeyValueListLength == 3):
            llist_object.fetch_All_list()
        else:
            ColumnName = KeyValueList[3]
            ColumnValue = KeyValueList[4]
            llist_object.fetch_list(ColumnName, ColumnValue, MetaData)

        return str(recordCount)

if __name__ == "__main__":
    app.run()