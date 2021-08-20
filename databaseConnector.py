import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='test')
if (cnx):
    print("Connection established")
else:
    print("Connection failed!")

def createTable():
    if(cnx):
        mycursor = cnx.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS RSSURLS (id int AUTO_INCREMENT, address VARCHAR(255) UNIQUE, subscribedChat VARCHAR(100), PRIMARY KEY(id))") #TODO add that only one chatId can be saved to one url
        print("Table created!")
    else:
        print("No active connection")


def insertAddress(url, chatID):
    mycursor = cnx.cursor()
    mycursor.execute("INSERT INTO RSSURLS (id, address, subscribedChat) VALUES ('NULL' , '" + url + "', '" + str(chatID) + "')")
    cnx.commit()

def updateSubscribedChat(url, chatID):
    mycursor = cnx.cursor()
    mycursor.execute("UPDATE RSSURLS SET subscribedChat = concat(subscribedChat, '" +','  + str(chatID) + "') WHERE address = '" + url + "'")
    cnx.commit()


def disconnect():
    if(cnx):
        cnx.close()
    else:
        print("No active connection!")
