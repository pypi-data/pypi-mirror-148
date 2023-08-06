import os
from expressdb.collection import Collection


class ExpressDB:
     def __init__(self, DB_NAME, DB_PASSWORD=None):

          self.__store = {}
          self.__password = DB_PASSWORD

          self.__information = {
               "default": "express-database",
               "name": DB_NAME.lower(),
               "password": self.__hidePassword(DB_PASSWORD),
               "collections": {
                    "total": len(list(self.__store.keys())),
                    "list": list(self.__store.keys())
               },
          }

          self.__storeConfigs = {
               "default": os.getcwd() + "/store/",
               "pathToCollectionStore": os.getcwd() + "/store/" + DB_NAME.lower() + "/"
          }

          self.__createStore()

     """PRIVATE FUNCTIONS"""

     def __getStore(self):
          return self.__store

     def __hidePassword(self, text):
          if text != None:
               encode = ""
               for i in text:
                    encode = encode + "*"
               return encode
          else:
               return text

     def __createStore(self):
          try:
               # create store
               if os.path.exists(self.__storeConfigs["default"]) == False:
                    os.mkdir(self.__storeConfigs["default"])

               # create collection store
               if os.path.exists(self.__storeConfigs["pathToCollectionStore"]) == False:
                    os.mkdir(self.__storeConfigs["pathToCollectionStore"])
          except ValueError:
               print(ValueError)

     def __isCollection(self, collection):
          """
               Check collection in store
               @params:
                    collection(type: str) -- the collection name
               @return boolean
          """
          try:
               store = self.__getStore()
               collections = list(store.keys())
               for element in collections:
                    if element == collection.lower():
                         return True
               return False
          except ValueError:
               print(ValueError)

     def __writeJSON(self, collection):
          file = open(
               self.__storeConfigs["pathToCollectionStore"] + collection.lower() + ".json", "w")

     def __createMessage(self, type, content):
          return {
               'type': type,
               'content': f"ExpressDB--[{type.upper()}]: {content}"
          }
     """USER FUNCTIONS"""
     def sayHello(self):
          pass

     def info(self):
          return self.__information

     def drop(self, collection):
          try:
               isComplete = False
               store = self.__getStore()
               isCollection = self.__isCollection(collection=collection)

               if isCollection:
                    del store[collection.lower()]
                    isComplete = True
                    if isComplete:
                         os.remove(
                         self.__storeConfigs["pathToCollectionStore"] + collection.lower() + ".json")
               else:
                    messages = self.__createMessage(
                         "error", f"Can not drop '{collection}' collection in database.")
                    print(f"{messages}")
               return isComplete

          except ValueError:
               print(ValueError)

     def create(self, collection, MODEL=None):
          try:
               store = store = self.__getStore()
               isCollection = self.__isCollection(collection=collection)

               if isCollection == False:
                    newCollection = Collection(
                         collection, MODEL, self.__storeConfigs)
                    store[collection.lower()] = newCollection
                    self.__writeJSON(collection)
                    return newCollection
               else:
                    message = self.__createMessage(
                         "error", f"Can not create a new collection.")
                    print(message)

          except ValueError:
               print(ValueError)

     def reset(self):
          try:
               isComplete = False

               print("DO YOU WANT TO RESET DATABASE? (y/n)")
               result = input("DO YOU WANT TO RESET DATABASE? (y/n): ")
               if result.lower() == "y" or result.lower() == "yes":
                    # Validate a existing pasword
                    if self.__password != None:
                         yourPassword = input(">> Input your password: ")
                         if self.__password == yourPassword:
                              self.__information.update({
                                   "name": self.__information["default"],
                                   "password": None
                              })
                              self.__store = {}
                              isComplete = True
                    else:
                         self.__information.update({
                                   "name": self.__information["default"],
                                   "password": None
                              })
                         self.__store = {}
                         isComplete = True

               return isComplete

          except ValueError:
               print(ValueError)

     def collection(self, collection):
          try:
               isCollection = self.__isCollection(collection=collection)
               if isCollection:
                    return self.__store[collection]
               else:
                    return None

          except ValueError:
               print(ValueError)

     def importCollection(self, path_to_file):
          """Import collection data from file to store
          """
          pass
