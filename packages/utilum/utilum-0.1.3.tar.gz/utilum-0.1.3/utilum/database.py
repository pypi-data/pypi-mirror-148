import sqlite3 as sq3

class Establish:
    def __init__(self, path, type="sqlite3"):
        self.type = type
        self.path = path
        self.connection = ""
        self.cursor = ""
        
        if(self.type == "sqlite3"):
            connection=sq3.connect(self.path)
            self.connection=sq3.connect(self.path)
            self.cursor=connection.cursor()            

    def getConnection(self):
        return self.connection, self.cursor