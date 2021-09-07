
def executeDBFragmentation():
    TableName = "DefaultDatabase"
    FileExtension = ".txt"
    FileName = TableName + FileExtension  # Framing the FileName

    # Reading the text file
    FileObject = open(FileName, 'r')
    Lines = FileObject.readlines()

    noOfTablesCount = 0
    for eachline in Lines:
        noOfTablesCount += 1

    tableSplitCount1 = int(noOfTablesCount/2)
    tableSplitCount2 = int(noOfTablesCount - tableSplitCount1)
    for eachline in Lines:
        if tableSplitCount1:
            FileName1 = "TablesAt_LocalDatabase.txt"
            f = open(FileName1, "a")
            f.write(eachline)
            f.close()
            tableSplitCount1 = tableSplitCount1 - 1
            continue

        if (tableSplitCount1 == 0 and tableSplitCount2):
            FileName2 = "TablesAt_RemoteDatabase.txt"
            f = open(FileName2, "a")
            f.write(eachline)
            f.close()
            tableSplitCount2 = tableSplitCount2 - 1

    FileObject = open(FileName, "r+")
    FileObject.truncate(0)
