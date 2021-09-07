import re
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary
from DBMS_Software.queryProcessor.GetPath import getPath

def deleteQueryParser():
    statement = input("Enter your Delete Statement: ")
    state = 0
    conditions = ""
    conditions_list = []
    x = statement.split(" ")
    table_name = ""
    tableLocation = ""
    # retrieving delete query tokens and check for validity of then
    print(x)
    if len(x) < 5:
        print("ERROR: Query should be like DELETE FROM table_name WHERE condition")
        return table_name, conditions_list, tableLocation
    elif x[0] != "DELETE":
        print("query should start from DELETE")
        return table_name, conditions_list, tableLocation
    elif x[1] != "FROM":
        print("query should be like DELETE FROM")
        return table_name, conditions_list, tableLocation
    elif x[3] != "WHERE":
        print('Incorrect syntax WHERE clouse missing or misplaced');
        return table_name, conditions_list, tableLocation
    else:
        for i in range(4, len(x)):
            conditions += x[i]
        table_name = x[2]
        condition_split = conditions.split(",", 200);
        for i in range(0, len(condition_split)):
            t = re.split('(\W)', condition_split[i])
            operator = ""
            for j in range(0, len(t)):
                if t[j] == "=" or t[j] == ">" or t[j] == "<":
                    operator += t[j]
                    t[j] = ""
            t.append(operator)
            t = list(filter(None, t))
        conditions_list = t

        tableLocation = readGlobalDataDictionary(table_name)

        try:
            fileExtension = '.txt'
            FileName = table_name + fileExtension

            if (tableLocation == 'RemoteLocation'):
                FilePath = FileName
            else:
                Path = getPath()
                FilePath = Path + FileName

            f = open(FilePath, 'r')
        except IOError:
            print("Table " + table_name + " is not available");

        print('\n')
        print('You Have Entered the Correct Syntax')
        print('\n')
        print('Please Wait........Your Request is being processed')
        print('\n')
        print('The Rows are Deleted...............')
        return table_name, conditions_list,tableLocation
