import shortuuid
import pandas
import json
import os


class Collection:

    DEFAULT_DATABASE_NAME = "ExpressDB"

    def __init__(self, collectionName, collectionModel, storeConfigs):

        self.__collectionName = collectionName.lower()
        self.__collectionModel = collectionModel
        self.__collectionData = []

        self.__storeConfigs = storeConfigs

    """
     """

    def __createMessage(self, type, content):
        return {
            'type': type,
            'content': f"ExpressDB--[{type.upper()}]: {content}"
        }

    def __gid(self, text):
        randomString = shortuuid.uuid()
        return f"{text}:{randomString[:20]}"

    def __checkSysIdKeyInObject(self, object):
        for key in list(object.keys()):
            if key == "_id":
                return True
            else:
                return False

    def __checkData(self, data):
        if type(data) == dict:
            for key in list(data.keys()):
                data[key] = type(data[key])
            return data == self.__collectionModel
        else:
            return False

    def __writeJSONFile(self, data):
        # data = []
        FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + \
            self.__collectionName + ".json"
        jsonString = json.dumps(data)
        jsonFile = open(FILE_COLLECTION, "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    def find(self, limit=0):
        try:
            if limit > 0:
                return self.__collectionData[0: limit]
            else:
                return self.__collectionData
        except ValueError:
            print(ValueError)

    def findById(self, document_id):
        try:
            isComplete = False

            for document in self.__collectionData:
                if document_id == document["_id"]:
                    isComplete = True
                    return document

            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not find data in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

        except ValueError:
            print(ValueError)

    def findObject(self, object):
        try:
            isComplete = False
            for document in self.__collectionData:
                if document == object:
                    return document
            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not find data in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

        except ValueError:
            print(ValueError)

    def insert(self, value):
        try:
            isComplete = False

            newModel = {}
            if type(value) == dict:
                for key in list(value.keys()):
                    newModel[key] = type(value[key])

            # remove sys_id key in value which added by user
            # then add new a sys_id key to document by system
            if self.__checkSysIdKeyInObject(value):
                value.update({"_id": self.__gid(self.__collectionName)})
            else:
                value["_id"] = self.__gid(self.__collectionName)

            if newModel == self.__collectionModel:
                self.__collectionData.append(value)
                isComplete = True
            elif self.__collectionModel == None:
                self.__collectionData.append(value)
                isComplete = True
            else:
                isComplete = False

            if isComplete:
                FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + \
                    self.__collectionName + ".json"
                if os.path.exists(FILE_COLLECTION):
                    writeFile = self.__writeJSONFile(self.__collectionData)

                message = self.__createMessage(
                    "info", f"Added value to '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
            else:
                message = self.__createMessage(
                    "error", f"Can not add new data to '{self.__collectionName}'. You must check model again. \n'{self.__collectionName}'.model is {self.__collectionModel}.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            return isComplete
        except ValueError:
            print(ValueError)

    def insertMany(self, values):
        pass
        # try:
        #      # values = []
        #      isComplete = False

        #      # new values after valid model
        #      validValues = []
        #      for value in values:
        #           newModel = {}
        #           if type(value) == dict:
        #                for key in list(value.keys()):
        #                     newModel[key] = type(value[key])
        #           if newModel == self.__collectionModel:
        #                validValues.append(value)

        #      for document in validValues:
        #           # remove sys_id key in value which added by user
        #           # then add new a sys_id key to document by system
        #           if self.__checkSysIdKeyInObject(document):
        #                document.update({"_id": self.__gid(self.__collectionName)})
        #           else:
        #                document["_id"] = self.__gid(self.__collectionName)

        #      self.COLLECTION_DATA = [ *self.__collectionData, *validValues]
        #      isComplete = True

        #      # Complete case
        #      if isComplete:
        #           # FILE_COLLECTION =  self.__storeConfigs["pathToCollectionStore"] + self.__collectionName +".json"
        #           # if  os.path.exists(FILE_COLLECTION):
        #           #      writeFile = self.__writeJSONFile(self.__collectionData)
        #           message = self.__createMessage("info", f"Added values to '{self.__collectionName}' collection.")
        #           print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

        #      return isComplete
        # except ValueError:
        #      print(ValueError)

    def updateById(self, document_id, newValue):
        # data = {}
        try:
            isComplete = False

            if self.__checkSysIdKeyInObject(newValue):
                del newValue["_id"]

            for document in self.__collectionData:
                if document['_id'] == document_id:
                    document.update(newValue)
                    isComplete = True
                    if isComplete:
                        FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + self.__collectionName + ".json"
                        if os.path.exists(FILE_COLLECTION):
                            self.__writeJSONFile(self.__collectionData)
                    message = self.__createMessage(
                        "info", f"Updated document in '{self.__collectionName}' collection.")
                    print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not update document in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            return isComplete

        except ValueError:
            print(ValueError)

    def updateObject(self, oldValue, newValue):
        try:
            isComplete = False

            if self.__checkSysIdKeyInObject(newValue):
                del newValue["_id"]

            for document in self.__collectionData:
                if document == oldValue:
                    document.update(newValue)
                    isComplete = True
                    if isComplete:
                        FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + \
                            self.__collectionName + ".json"
                        if os.path.exists(FILE_COLLECTION):
                            self.__writeJSONFile(self.__collectionData)

                    message = self.__createMessage(
                        "info", f"Updated document in '{self.__collectionName}' collection.")
                    print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not update document in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            return isComplete
        except ValueError:
            print(ValueError)

    def deleteById(self, document_id):
        try:
            isComplete = False

            for document in self.__collectionData:
                if document_id == document["_id"]:
                    self.__collectionData.remove(document)
                    isComplete = True
                    if isComplete:
                        FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + \
                            self.__collectionName + ".json"
                        if os.path.exists(FILE_COLLECTION):
                            writeFile = self.__writeJSONFile(
                                self.__collectionData)
                    message = self.__createMessage(
                        "info", f"Deleted document in '{self.__collectionName}' collection.")
                    print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not delete document in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            return isComplete

        except ValueError:
            print(ValueError)

    def deleteObject(self, object):
        try:
            isComplete = False

            for document in self.__collectionData:
                if document == object:
                    self.__collectionData.remove(document)
                    isComplete = True
                    if isComplete:
                        FILE_COLLECTION = self.__storeConfigs["pathToCollectionStore"] + \
                            self.__collectionName + ".json"
                        if os.path.exists(FILE_COLLECTION):
                            writeFile = self.__writeJSONFile(
                                self.__collectionData)
                    message = self.__createMessage(
                        "info", f"Deleted document in '{self.__collectionName}' collection.")
                    print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            # Fail case
            if isComplete == False:
                message = self.__createMessage(
                    "error", f"Can not delete document in '{self.__collectionName}' collection.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")

            return isComplete
        except ValueError:
            print(ValueError)

    def truncate(self):
        try:
            isComplete = False
            self.__collectionData = []
            isComplete = True
            if isComplete:
                message = self.__createMessage(
                    "info", f"'{self.__collectionName}' collection is empty.")
                print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
            return isComplete
        except ValueError:
            print(ValueError)

    def select(self):
        dataframe = pandas.DataFrame(self.__collectionData)
        print(dataframe)

    def model(self):
        if self.__collectionModel != None:
            message = self.__createMessage(
                "info", f"Properties's '{self.__collectionName}': {self.__collectionModel}.")
            print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
        else:
            message = self.__createMessage(
                "info", f"Properties's '{self.__collectionName}': NONE.")
            print(f"{self.DEFAULT_DATABASE_NAME}'s message: {message}")
