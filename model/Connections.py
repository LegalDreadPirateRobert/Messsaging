import Connections as cons
import Connection from Connection as Con
from time import sleep
class Connections:
    self.connections = []
    
    def toBeMessaged(self):
        x = open(cons.TO_BE_MESSAGED_FILE_PATH,"r");
        if x.read() == "":
            x.close()
            return True
        x.close()
        return False
        
    def getConnection(self,brow,sel,soup):
        page = cons.CONNECTIONS_PAGE
        i = 1
        page+=i
        retrys = 0
        while i < 100:
            brow.get(page)
            PAGE_RESULT = self.getConnections(brow,soup)
            if PAGE_RESULT == None:
               if retrys > 4:
                   break
               retrys+=1
               continue
            page = page[0:-1]
            self.addConnection(PAGE_RESULT)
            i+=1
        
    def getConnections(self,brow,soup):
        soup = soup()
        x = soup.findAll("a", {"class": cons.CONNECTION_CONTAINER })
        ctr = 0
        new_connection = []
        ctr = 0
        for i in x:
            connectionName = i.find("img")
            if ctr % 2 == 0:
                if connectionName:
                    print(connectionName["alt"])
                    print(i["href"])    
                    new_connection.append(Connection(connectionName["alt"],i["href"]))
                else:
                    new_connection.append(Connection(None,i["href"]))
            ctr+=1
        return new_connection

    def addConnection(self,res):
        connection_file = open(cons.CONNECTION_FILE_PATH,"a")
        toBeMessaged_file = open(cons.TO_BE_MESSAGED_FILE_PATH,"a")
        for i in res:
            connection_file.write( f"{i.name} {i.profile} \n")
            toBeMessaged_file.write( f"{i.name} {i.profile} \n")
        toBeMessaged_file.close()
        connection_file.close()

    def loadConnections(self):
        toBeMessagedConnections = []
        with open(cons.TO_BE_MESSAGED_FILE_PATH) as file_in:
             test = " "
             for line in file_in:
                person = line.split()
                toBeMessagedConnections.append(Connection(person[0],person[1]))
        return toBeMessagedConnections