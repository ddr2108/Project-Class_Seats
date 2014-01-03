import sys
import datetime
import time
from googlevoice import Voice
from bs4 import BeautifulSoup
import urllib2

###############################################################################
########################Initial Setup##########################################
#Google Voice
source = "Deep Datta Roy:"      #holds the number which is the source
number = "4045148059"           #the actual number
email = "deepdattaroy8888@gmail.com"    #login info
pwd = "####"
#Class URL
base = "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=201402&crn_in="
CRNName = ["Network", "Test", "Mobile Services", "SW DEV", "Net Sec(=/)", "Adv Internet"]
CRN = [27006, 27007, 27013, 29311, 21268, 27011]
timer = [0,0,0,0]
timeout = 1200;

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
    for index in range(0,len(CRN)):
        classCRN = CRN[index]
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
            if int(message.get_text()) > 0 and timer[index] == 0:
                information = str(classCRN) + " (" + CRNName[index] +  ") "+ " is available"
                timer[index] = timeout;
                sendSMS(information)
            elif int(message.get_text()) > 0:
                timer[index] = timer[index] - 1

#send requested data via SMS
def sendSMS(data):
    global voice
    
    voice.send_sms(number, data)

if __name__=="__main__":
    main()
