import os
import sys
import string
import operator
import re
from functions import *
from html import *

def main():
    if len(sys.argv) != 2:                                      #Validate command line arguments ###(specification 1.0.X)###
        failcommandline()                                                  
    if not os.path.isfile(sys.argv[1]):
        failcommandline() 
    path=sys.argv[1]
    filename=os.path.basename(path)
    basename=os.path.basename(path)
    dotloc=basename.find(".")
    basename=basename[:dotloc]
                                                                #Opens two copies of the bin file for reading
    finone=open(path,'rb')                                      #We use two because some processing for phone details seems to interfere
    fintwo=open(path,'rb')                                      #With the processing of text messages so this seemed like a good fix
    
    #A list of years to look for. This is useful since dates are the initial indicators of phone communications and the dates start with years
    years=['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013']
    predata=[]
    outdata=[]
    
    #Functions to find phone details
    phoneinfolist=phonedetails(finone)                          #Finds brand, manufacturer, version, ect ###(specification 3.0.1)###
    outdata.append(phoneinfolist)                               #Adds phone details as a list to the main output file

    #Error messages from not using this program on an appropriate cell phone type
    if "Product Brand: verizon" not in phoneinfolist:
        failphonetype()

    #The start of processing for phone communications
    splitfilelist=[]
    for line in fintwo:                                         #Searches every line of the bin file
        for year in years:                                      #Searches every year in the above years list
            yearcount=line.count(year+'-')                      #Counts the occurrences of specific years with a dash after it
            while yearcount>1:                                  #While there are any instances of the year-
                lastyearloc=line.rfind(year+'-')                #It finds the location of the furthest right year-
                newline=line[lastyearloc:]                      #Create a new line from the year to the end of the line
                line=line[:lastyearloc]                         #Reassign line to the same thing as before minus the last year- and everything that followed it
                yearcount=line.count(year+'-')                  #It counts the number of times a year- appears in the line
                newline=remove_nonmsg(newline)                  #The first thing that appears after the text message or phone number are invalid characters...
                                                                    #These are detected and removed by our remove_nonmsg function.###(specification 3.0.2)###
                if newline is not None:                         
                    splitfilelist.append(newline)               #Appends newline to outdata if it has content

    for line in splitfilelist:
        date=str(line[0:10])                                    #Trims the date off and assigns it a variable name date ###(specification 4.0.1)###
        time=str(line[11:19])                                   #Trims the time off and assigns it a variable name time ###(specification 4.0.1)###
        msg=str(line[19:])                                      #Assigns everything else on the line the variable name msg ###(specification 5.0.1)###
        msg.replace("  "," ")                                   #Gets rid of overly long spaces between characters
        phone=""                                                #Initializes string for phone number
        name=""                                                 #Initializes string for the name of the person they are calling
        phonepos=phonepatern(msg)                               #Calls function to determine the phone number ###(Specification 2.0.X)###
        if phonepos is not None:
            phone=phonepos
        name=getname(msg, phone)                                #Our getname function gets the name of the person being called
        if len(phone)==20:                                      #For calls that don't have a name assigned to the number it gives the number...
            half=len(phone)/2                                       #twice so we just take half the number
            phone=phone[:half]
        if phone and name:
            texttuple=(date, time, phone, name)                 #Since text messages and phone numbers are on different lines we made two tuple types...
            predata.append(texttuple)                               #The tuples of four strings which have the name and number
        else:
            texttuple=(date, time, msg)                             #and tuples of three strings which have the text message
            if msg is not None:
                predata.append(texttuple)                       #Both tuple types are appended to a list named predata (here and above four lines)
                
    sorteddata=sortdata(predata)                                #The tuples are sent to our sortdata function ###(specification 5.0.1)###                      
    outdata.append(sorteddata)                                  #The sorted and processed data is appended to the main output file as a list (outdata is now a list of two lists)
    phoneinfo=outdata[0]                                        #First list from outdata (the phone info from near the begining)
    textinfo=outdata[1]                                         #Second list from outdata (the text and phone number info)
    createOutputFile(phoneinfo, textinfo)                       #For printing to an html file ###(Specification 7.0.X - 10.0.X)###
    finone.close()                                              #Closes the two input files we opened earlier
    fintwo.close()

def failcommandline():                                          #Error message for command line argument errors
    print "Missing or invalid argument."
    print "Please enter the name of a '.bin' file."
    print "Examples of usage:"
    print "phonesearch.py nokia.bin"
    print "If the path has a space, use quotation marks."
    print '"phone search.py"'
    sys.exit(-1)
    
def failphonetype():                                            #Error message for inappropriate phone type
    print "Error: This program has only been proven to work on Verizon Eris cell phones"
    sys.exit(-1)
    
main()

