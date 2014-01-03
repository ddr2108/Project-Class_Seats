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
#Class URL
base = "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=201402&crn_in="
CRN = [20191 , 27006, 24834, 29945]
timer[]
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
        processClass()                   #Process Recieved Messages
        time.sleep(3)

#Get class info and process
def processClass():
    global timer

    #Break each message into words
    for index in range(1:len(CRN)):
        classCRN = CRN[index]
        print classCRN
        #Send and Receive class data
        url = base + str(classCRN)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        page = response.read()
        #Parse the data
        tree = BeautifulSoup(page)           #convert to beautiful soup object
        messages = tree.findAll("td","dddefault")     #find all texts and pull data
        for message in messages[3:4]:
            #check if seat available 
            if int(message.get_text()) > 0:
                information = str(classCRN) + " is available:\n" + url
                sendSMS(information)

#send requested data via SMS
def sendSMS(data):
    voice.send_sms(number, data)

if __name__=="__main__":
    main()