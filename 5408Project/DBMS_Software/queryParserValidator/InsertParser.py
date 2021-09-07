import os
import re

def validateInsertStatement():
    statement = input("Enter your Insert Statement: ")
    datatype_list = ['int', 'varchar', 'double']
    data_added_list = []
    if '(' not in statement:
        print("ERROR: Query should start like INSERT INTO TABLENAME")
    else:
        path = "C:/99.DATABASE/ddms_group19/5408Project/DBMS_Software/queryProcessor/"
        x=statement.split("(")
        # splitting the create sql query into two parts 'CREATE TABLE TABLENAME', 2nd part rest of query
        first_part = x[0].split(" ");
        if(len(first_part) == 3 or len(first_part) == 4):
            path = path + first_part[2] + ".txt"
            if(first_part[0].upper()!="INSERT" and first_part[1].upper()!="INTO"):
                print("ERROR: Query should start from INSERT INTO")

            elif (os.path.isfile(path)):
                if(len(first_part)==4 and first_part[3].upper()=="VALUES"):
                    if ')' in x[1]:

                        # Removing last ');
                        x[1] = x[1].split(")")[0]

                        if ',' in x[1]:

                            # Opening file metadata to check the datatypes
                            filenamemeta = first_part[2]+"Metadata.txt"
                            filename = first_part[2]+".txt"
                            openmeta = open(filenamemeta, "r")

                            # Opening table file to insert values
                            opentable = open(filename, "a+")
                            countlines=0
                            content = openmeta.read()
                            CoList = content.split("\n")

                            for i in CoList:
                                if i:
                                    countlines += 1
                            second_part=x[1].split(",")

                            # Checking if metadata variables number and provided in insert statement are same
                            if(len(second_part)==countlines):
                                lines = open(filenamemeta, 'r').readlines()
                                countlines=0
                                linenumber=0
                                # Checking each line datatype from metadata and checking with user provided input for insert
                                for line in lines:
                                    linenumber+=1
                                    eachline = line.strip().split(" ")[1]
                                    eachlist = second_part[countlines]
                                    flag = "correct"
                                    if(len(line.strip().split(" "))>3):
                                        if(line.strip().split(" ")[2]=="PRIMARY" and line.strip().split(" ")[3]=="KEY"):

                                            lines_table = open(filename, 'r').readlines()
                                            for line_table in lines_table:
                                                fetchvalue = line_table.split('^')[countlines]
                                                if(fetchvalue ==  eachlist):
                                                    flag ="incorrect"
                                                    print("PRIMARY KEY VIOLATION")
                                                    break
                                            if(flag == "incorrect"):
                                                break
                                    # Check if user provided int input for variable INT in metadata
                                    if(eachline.upper() == 'INT' and re.match('^[0-9]*$', eachlist)):

                                        data_added_list.append(eachlist)

                                    # Check if user provided string input for variable VARCHAR in metadata
                                    elif (eachline.upper().find("VARCHAR") != -1 and eachlist[0]=="'"and eachlist[-1]=="'"):

                                        if(eachlist[1:-1].isalpha()):
                                            flag="correct"
                                            data_added_list.append(eachlist[1:-1])
                                        else:
                                            flag="incorrect"
                                            break
                                    else:
                                        print(eachlist[1])
                                        eachlist[-1]
                                        flag = "incorrect"
                                        break
                                    countlines += 1
                                # If flag value is correct only than writing into file.
                                if(flag=="correct"):
                                    return first_part[2],data_added_list

                                else:
                                    print("ERROR7: DATA NOT PROVIDED CORRECTLY")
                                data_added_list.clear()

                            else:
                                print("ERROR6: INCORRECT LENGTH DEFINED..")
                        else:
                            print("ERROR1: QUERY IS INCORRECT..")
                    else:
                        print("ERROR2: QUERY IS INCORRECT..")
                else:
                    print("ERROR3:QUERY IS INCORRECT..")

            else:
                print("ERROR4: FILE NAME IS NOT CORRECT.")

        else:
            print("ERROR5: Query is not in correct format")
    return '', ''
# SAMPLE QUERY - INSERT INTO Person values(1,'Steward','Peter','Canada','Halifax');
# SAMPLE QUERY - INSERT INTO person(PersonID,LastName,FirstName,Address,City) values(1,'Steward','Peter','Canada','Halifax');
# INSERT into PeopleRecord values(2,'Aparna','Chennai')
