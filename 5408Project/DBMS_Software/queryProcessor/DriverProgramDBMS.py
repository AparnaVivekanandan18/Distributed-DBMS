from DBMS_Software.queryProcessor.DisplayERD import displayERD
from DBMS_Software.queryProcessor.ProcessInsertQuery import executeInsert
from DBMS_Software.queryProcessor.ProcessSelectQuery import executeSelect
from DBMS_Software.queryProcessor.ProcessUpdateQuery import executeUpdate
from DBMS_Software.queryProcessor.ProcessDeleteQuery import executeDelete
from DBMS_Software.queryParserValidator.CreateParser import validateCreateStatement
from DBMS_Software.queryParserValidator.InsertParser import validateInsertStatement
from DBMS_Software.queryProcessor.DatabaseFragmentation import executeDBFragmentation
from DBMS_Software.queryProcessor.FormGlobalDataDictionary import formGDD
import base64

from DBMS_Software.queryProcessor.SQLDump import createSQLDump


def main():
    print("\n")
    print("............................................WELCOME!....................................................")
    print("Are you the DBA Client? If so type Y : Else type N")
    type_of_user = input()

    print("USERNAME:")
    uname = input()
    print("PASSWORD:")
    password = input()

    encrypted_password = base64.b64encode(bytes(password, 'utf-8'))
    authentication_file = open('Authentication.txt', 'r')
    credentials = authentication_file.readlines()
    if (type_of_user == "Y"):
        if (uname == credentials[0].split("^")[0] and base64.b64decode(encrypted_password) == base64.b64decode(credentials[0].split("^")[1])):
            print("WELCOME TO DATABASE ADMINISTRATION CONFIGURATION")
            print("Press 1 for DataBaseFragmentation")
            print("Press 2 for Creating Global Data Dictionary")
            print("Press 3 for Downloading SqlDumb")
            print("Press 4 for Entity Relationship Diagram")
            dba_input = input()
            if(dba_input == '1'):
                executeDBFragmentation()
                print("Database Fragmentation is Done")
                return
            if(dba_input == '2'):
                formGDD()
                print("Global Data Dictionary Creation is Done")
                return
            if(dba_input == '3'):
                createSQLDump()
                print("SQL DUMP IMPORTED")
                return
            if(dba_input == '4'):
                displayERD()
                return
            else:
                print("Relax")

        else:
            print("Your Credentials are Invalid....Try Again...Sorry!")
            main()

    if (type_of_user == "N"):
        if (uname == credentials[1].split("^")[0] and base64.b64decode(encrypted_password) == base64.b64decode(credentials[1].split("^")[1])):
            print("WELCOME TO SQL PROCESSING......................................................................")
            print('\n')
            print("Press 1 for CREATE")
            print("Press 2 for INSERT")
            print("Press 3 for DELETE")
            print("Press 4 for UPDATE")
            print("Press 5 for SELECT")
            print("Enter the Operation you want to perform:")
            USER_INPUT = input()

            if (USER_INPUT == '1'):
                validateCreateStatement()
                return
            if (USER_INPUT == '2'):
                executeInsert();
                return
            if (USER_INPUT == '3'):
                executeDelete()
                main()
                return
            if (USER_INPUT == '4'):
                executeUpdate()
                return
            if (USER_INPUT == '5'):
                executeSelect()
                main()
                return
            if(USER_INPUT != "1" or USER_INPUT != "2" or USER_INPUT != "3" or USER_INPUT != "4" or USER_INPUT != "5"):
                print("Enter the proper valid operation")
        else:
            print("Your Credentials are Invalid....Try Again...Sorry!")
            main()

main()
