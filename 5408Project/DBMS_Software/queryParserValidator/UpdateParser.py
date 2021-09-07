import re
from DBMS_Software.queryProcessor.ReadGlobalDataDictionary import readGlobalDataDictionary
from DBMS_Software.queryProcessor.GetPath import getPath

def updateQueryParser():
    statement = input("Enter your Update Statement: ")
    state = 0
    conditions = ""
    conditions_list = []
    set_split = []
    table_name = ""
    column_list = []
    tableLocation = ""

    statement_duplicate = statement
    x = re.search("^UPDATE.* SET.* WHERE.*", statement)

    if x:
        print("Correct syntax")
        set_split = statement_duplicate.split("SET")
        table_name = set_split[0].split(" ")[1];
        where_split = set_split[1].split("WHERE")

        # Splitting all the characters and operators for column list and conditions list
        column_list = re.split('=', where_split[0])
        column_list = [item.strip() for item in column_list]

        condition_split = where_split[1].split(",", 200);
        for i in range(0, len(condition_split)):
            t = re.split('(\W)', condition_split[i])
            operator = ""
            for j in range(0, len(t)):
                if t[j] == "=" or t[j] == ">" or t[j] == "<":
                    operator += t[j]
                    t[j] = ""

            t.append(operator)

            # Removing blank elements from list
            t = list(filter(None, t))

            # Removing white spaces from list
            for ele in t:
                if ele.strip():
                    conditions_list.append(ele)

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
                    updateQueryParser()
        except IOError:
            print("Table " + table_name + " is not available");
            updateQueryParser();
        return table_name ,column_list ,conditions_list,tableLocation

    else:
        print("ERROR: Query should be like UPDATE TABLE table_name SET column1 = value1, column2 = value2, ... WHERE "
              "condition")
        return table_name ,column_list ,conditions_list,tableLocation