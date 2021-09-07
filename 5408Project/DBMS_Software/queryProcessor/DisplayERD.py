from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import fetchFileFromGCP
def displayERD():
    print("Enter the No of Tables you want to Establish a Relationship:")
    noOfTables = int(input())

    TableNames = []
    for i in range (0,noOfTables):
        print("Enter the TableName:")
        Table = input()
        TableNames.append(Table)

    #Primary Keys
    listOfAllPrimaryKeys = []
    for i in range(0, noOfTables):
        TableName = TableNames[i]
        FileExtension = ".txt"
        FileName = TableName + FileExtension  # Framing the FileName
        metaFileExtension = 'Metadata.txt'
        metaDatafileName = TableName + metaFileExtension

        # Reading the text file
        FileObject = open(metaDatafileName, 'r')
        Lines = FileObject.readlines()

        for eachline in Lines:
            primaryKey = 'PRIMARY'
            result = eachline.find(primaryKey)
            if (result>0):
                TableColumnValue = eachline.split(' ')
                primaryKeyColumnName = TableColumnValue[0]
                listOfAllPrimaryKeys.append(primaryKeyColumnName)



    #Foreign Key Check
    listOfAllForeignKeys = []
    for i in range(0, noOfTables):
        TableName = TableNames[i]
        FileExtension = ".txt"
        FileName = TableName + FileExtension  # Framing the FileName
        metaFileExtension = 'Metadata.txt'
        metaDatafileName = TableName + metaFileExtension

        # Reading the text file
        FileObject = open(metaDatafileName, 'r')
        Lines = FileObject.readlines()


        TableColumnValue = []
        for eachline in Lines:
            foreignKeyTest = 'REFERENCES'
            result = eachline.find(foreignKeyTest)
            if (result>0):
                res = eachline.partition(foreignKeyTest)[2]
                mod_string = res[:-1]
                TableColumnValue = mod_string.split('(')
                ReferencedTableName = TableColumnValue[0]
                ColumnName = TableColumnValue[1]
                ColumnName = ColumnName[:-1]
                print('---------------------------------------------------------------------')
                print('ENTITY NAMES')
                print(TableNames[i])
                print(ReferencedTableName)
                print('---------------------------------------------------------------------')
                print('REFERENCED COLUMN NAME FOR ENTITIES:' + TableNames[i] + ReferencedTableName)
                print(ColumnName + '---> Establishes Relationship between the above mentioned Entities')

                FileObject = open('ERD_Status','a+')
                FileObject.write('Entities---->' + '\t' + TableNames[i] + ReferencedTableName + '\n' + 'Relationship---->' + '\t' + ColumnName)
                FileObject.close()

                listOfAllForeignKeys.append(ColumnName)