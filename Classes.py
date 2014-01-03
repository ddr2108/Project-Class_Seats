import sys
import datetime
import time
from googlevoice import Voice
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urllib2

###############################################################################
########################Initial Setup##########################################
#Google Voice
source = "Deep Datta Roy:"      #holds the number which is the source
number = "4045148059"           #the actual number
email = "deepdattaroy8888@gmail.com"    #login info
pwd = "5891Deep"
#Database
ip = 'localhost'
port = 27017
###############################################################################
###############################################################################

#Global Variables
prevTransaction = -1           #holds the number of messages earlier
voice = -1                     #holds the Google Voice Interface

#main function
def main():
    global voice

    #Google Voice Interface
    voice = Voice()
    voice.login(email,pwd)              #Login
    while True:
        voice.sms()                     #Get SMS Data  
        messages = extractSMS(voice.sms.html)      #Get messages
        processMessages(messages)                   #Process Recieved Messages
        time.sleep(30)

#processes the recieved messages
def processMessages(messages):
    #Break each message into words
    for message in messages:
        messagePieces = message.split()
        print 1
        #if 4 words, do more processing
        if (len(messagePieces)==4 and messagePieces[0].lower() =="ledger"):
            insertDB(messagePieces)
            sendSMS("Transaction Added")
        elif (len(messagePieces)==2 and messagePieces[0].lower() =="ledger"):
            data = requestDB(messagePieces)
            textToSend = "Spent: $" + str(data)
            sendSMS(textToSend)

#send requested data via SMS
def sendSMS(data):
    voice.send_sms(number, data)

    return messagesNew

if __name__=="__main__":
    main()