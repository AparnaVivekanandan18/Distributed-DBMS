from google.cloud import storage
import os
def formGDD():
    FileName = "TablesAt_RemoteDatabase.txt"
    FileLocation = "RemoteLocation"
    createGlobalDataDictionary(FileName,FileLocation)
    pushRemoteFilesToGCP(FileName)
    f = open(FileName, "r+")
    f.truncate(0)

    FileName = "TablesAt_LocalDatabase.txt"
    FileLocation = "LocalSystem"
    createGlobalDataDictionary(FileName,FileLocation)
    f = open(FileName, "r+")
    f.truncate(0)

def createGlobalDataDictionary(FileName,FileLocation):
    FileObject = open(FileName, 'r+')
    Lines = FileObject.readlines()

    for eachline in Lines:
        GDDFile = "GlobalDataDictionaryFile.txt"
        fGDDFile = open(GDDFile, 'a+')
        line = eachline[:-1]
        newline = line+' '+FileLocation
        fGDDFile.write(newline+'\n')
        fGDDFile.close()

def pushRemoteFilesToGCP(FileName):
    FileObject = open(FileName, 'r+')
    Lines = FileObject.readlines()

    for eachline in Lines:
        #initialPath = 'queryProcessor/'
        fileExtension = '.txt'
        metaFileExtension = 'MetaData.txt'
        eachline = eachline[:-1]
        fileToBeUploaded = eachline+fileExtension
        metaFileToBeUploaded = eachline+metaFileExtension

        # Setting credentials using the downloaded JSON file
        client = storage.Client.from_service_account_json(json_credentials_path='river-daylight-305308-178d865deb2e.json')
        # Creating bucket object
        bucket = client.get_bucket('distributeddb')
        # Name of the object to be stored in the bucket
        object_name_in_gcs_bucket = bucket.blob(fileToBeUploaded)
        object_name2_in_gcs_bucket = bucket.blob(metaFileToBeUploaded)
        # Name of the object in local file system
        object_name_in_gcs_bucket.upload_from_filename(fileToBeUploaded)
        object_name2_in_gcs_bucket.upload_from_filename(metaFileToBeUploaded)
        #Drop the Existing table (.txt) in the location
        os.remove(fileToBeUploaded)
        os.remove(metaFileToBeUploaded)