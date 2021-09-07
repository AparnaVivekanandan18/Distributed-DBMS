import os

from datetime import datetime
def validateCreateStatement():
  statement = input("Enter your Create Statement: ")
  datatype_list = ['INT', 'VARCHAR', 'DATETIME']
  if '(' not in statement:
     print("ERROR: Query should start like CREATE TABLE TABLENAME")
  else:
        x=statement.split("(",1)
        # splitting the create sql query into two parts 'CREATE TABLE TABLENAME', 2nd part rest of query
        first_part = x[0].strip()
        first_part_split=first_part.split(" ")
        #Checking if query starts with CREATE TABLE TABLENAME
        if ((first_part_split[0].upper() !="CREATE") or (first_part_split[1].upper() !="TABLE")) :
          print("ERROR: Query should start like CREATE TABLE TABLENAME")
        elif (len(first_part_split)!=3 or len(first_part_split[2])==0 ) :
          print("ERROR: QUERY IS NOT IN CORRECT FORMAT")
        # Tablename must not contain special character
        elif first_part_split[2].isalpha():
          #  if first part is correct, checking second part of query where we are checking for datatype is correct for each.
          second_part = x[1]
          second_part=second_part[:-1]
          second_part_split=second_part.split(",")
          syntax_incorrect=0
           #Storing each part in list like ['PersonID int','LastName varchar(255)']
          for i in second_part_split:
              syntax_incorrect=0
              i=i.strip()
              column_split = i.split(" ")
              if (any(ele in column_split[1].upper() for ele in datatype_list) and (column_split[0].isalpha()) and (len(column_split)==2 or (len(column_split)==4 and column_split[2].upper() =="PRIMARY" and column_split[3].upper() =="KEY" ) )):
                syntax_incorrect=0
              elif (any(ele in column_split[1].upper() for ele in datatype_list) and (column_split[0].isalpha()) and (len(column_split)==2 or (len(column_split)==6 and column_split[2].upper() =="FOREIGN" and column_split[3].upper() =="KEY" and column_split[4].upper() =="REFERENCES") )):
                path = "C:/99.DATABASE/ddms_group19/5408Project/DBMS_Software/queryProcessor/"
                filename = column_split[5].split("(")[0] + "Metadata.txt"
                path = path + filename
                reference_column_foreign_key = column_split[5].split("(")[1].split(")")[0]
                if(os.path.isfile(path)):
                    open_reference_file = open(filename,'r')
                    Lines = open_reference_file.readlines()
                    flag = 0
                    for line in Lines:
                        line = line.split(" ")[0]
                        if(line == reference_column_foreign_key ):
                            flag = 1
                            break
                        else:
                            flag = 0
                    if(flag == 1):
                        syntax_incorrect = 0
                    else:
                        syntax_incorrect = 1
                        break
                else:
                    syntax_incorrect = 1
                    break
              else:
                syntax_incorrect=1
                break
          if(syntax_incorrect == 0):
            print("CORRECT FORMAT IDENTIFIED.. TABLE CREATED SUCCESSFULLY..")
            filename = "%s.txt" % first_part_split[2]
            file = open(filename,"w")
            file.close()
            TableName = first_part_split[2]
            NumOfRecords = str(0)
            DateTime = str(datetime.now())
            DateTime = "".join(DateTime.split())
            LogFileName = "GeneralLog.txt"
            logfile = open(LogFileName, 'a+')
            logfile.write(TableName + ' ' + NumOfRecords + ' ' + DateTime + "\n")
            logfile.close()
            Event = 'CREATE'
            EventLogFile = "EventLog.txt"
            EventLogFile = open(EventLogFile,'a+')
            EventLogFile.write(TableName + ' ' + Event + ' ' + DateTime + "\n")
            EventLogFile.close()
            # creating metadata file saving each column details and datatype
            metafilename = first_part_split[2]+"Metadata.txt"
            metafile = open(metafilename, "w")
            for i in second_part_split:
                metafile.write(i+"\n")
            metafile.close()
          else:
            print("INCORRECT FORMAT IDENTIFIED.. TABLE CREATION FAILED..")
        else:
            print("ERROR: QUERY IS NOT IN CORRECT FORMAT")
#res = validateCreateStatement(val)
# SAMPLE QUERY CREATE TABLE (PersonID int,LastName varchar(255),FirstName varchar(255),Address varchar(255),City varchar(255));
# Create table People(PeopleID int PRIMARY KEY,PeopleName varchar(50),Address varchar(100) FOREIGN KEY REFERENCES FACULTY(facultyId))
# create table employees(name varchar(50),id int,address varchar(250))