import re
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary
from DBMS_Software.queryProcessor.GetPath import getPath


def selectQueryParser():
    statement = input("Enter your Select Statement: ")
    state = 0
    conditions = ""
    conditions_list = []
    table_name = ""
    tableLocation = ""
    if 'WHERE' not in statement:
        x = statement.split(" ")
        if len(x) < 4:
            print("ERROR: Query should be like SELECT * FROM table_name OR SELECT * FROM table_name WHERE condition")
            return table_name, conditions_list, tableLocation
        elif x[0] != "SELECT":
            print("query should start from SELECT")
            return table_name, conditions_list, tableLocation
        elif x[1] != "*":
            print("query should be like SELECT * FROM")
            return table_name, conditions_list, tableLocation
        elif x[2] != "FROM":
            print("query should be like SELECT * FROM")
            return table_name, conditions_list, tableLocation
        else:
            print("Correct syntax")
            print("Table Name ", x[3])
            table_name = x[3]

            tableLocation = readGlobalDataDictionary(table_name)

            try:
                fileExtension = 'Metadata.txt'
                FileName = table_name + fileExtension

                if (tableLocation == 'RemoteLocation'):
                    FilePath = FileName
                else:
                    Path = getPath()
                    FilePath = Path + FileName

                if (tableLocation != 'RemoteLocation'):
                    f = open(FilePath, 'r')
            except IOError:
                print("Table " + table_name + " is not available");
                selectQueryParser()

            print('\n')
            print('You Have Entered the Correct Syntax')
            print('\n')
            print('Please Wait........Your Request is being processed')
            print('\n')
            print('Search Query Request Results')
            return table_name, conditions_list, tableLocation

    else:
        x = statement.split(" ")
        # retrieving delete query tokens and check for validity of then

        if len(x) < 4:
            print("ERROR: Query should be like SELECT * FROM table_name OR SELECT * FROM table_name WHERE condition")
        elif x[0] != "SELECT":
            print("query should start from SELECT")
            return table_name, conditions_list, tableLocation
        elif x[1] != "*":
            print("query should be like SELECT * FROM")
            return table_name, conditions_list, tableLocation
        elif x[2] != "FROM":
            print("query should be like SELECT * FROM")
        elif x[4] != "WHERE":
            print("Where statement is misplaced")
        else:
            for i in range(5, len(x)):
                conditions += x[i]
            table_name = x[3]
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
                fileExtension = 'Metadata.txt'
                FileName = table_name + fileExtension

                if (tableLocation == 'RemoteLocation'):
                    FilePath = FileName
                else:
                    Path = getPath()
                    FilePath = Path + FileName

                if (tableLocation != 'RemoteLocation'):
                    f = open(FilePath, 'r')
                    columns = f.readlines()
                    for i in range(0, len(columns)):
                        columns[i] = columns[i].split(" ")[0]
                    if conditions_list[0] not in columns:
                        print("Invalid column name " + conditions_list[0])
            except IOError:
                print("Table " + table_name + " is not available")
                selectQueryParser()

            print('\n')
            print('You Have Entered the Correct Syntax')
            print('\n')
            print('Please Wait........Your Request is being processed')
            print('\n')
            print('Search Query Request Results')
            return table_name, conditions_list, tableLocation