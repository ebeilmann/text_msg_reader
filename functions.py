import os
import sys
import string
import operator
import re

################################# process text message methods ################################# Specification Optional
#sorts tuples by date and time then matches callers and their phone numbers to the text messages
def sortdata(filelist): # Specification optional
    msgdata=[]
    numdata=[]
    #Breaks up tuples for easy sorting and matching of text with caller(rejoined together further down)
    for tup in filelist:
        if len(tup)==4:
            date,time,phone,name=tup                            #splits up the tuple
            sdate=date.split('-')                               #splits the date into three different numbers
            stime=time.split(':')                               #splits time into three different numbers
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],phone,name)
                numdata.append(newtup)                          #Repacks the tuples with the now seperated dates and times
        if len(tup)==3:
            date,time,message=tup                               #splits up the tuple
            sdate=date.split('-')                               #splits the date into three different numbers
            stime=time.split(':')                               #splits time into three different numbers
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],message)
                msgdata.append(newtup)                          #Repacks the tuples with the now seperated dates and times
                
    #Combines text messages with the caller and phone number           
    combinelist=[]
    for msg in msgdata:                                         #For every tuple in the list with text messages
        for num in numdata:                                     #For every tuple in the list with numbers and names
            if num[:5]==msg[:5]:                                #If a message tuple and a number tuple have a matching year, month, day, hour, and minute they are...
                combinetuple=(num[0],num[1],num[2],num[3],num[4],num[5],msg[6],num[7],num[6])#combined into a single tuple 
                combinelist.append(combinetuple)                #the combined tuple is 
                    
    combinelist=sorted(combinelist, key=operator.itemgetter(0,1,2,3,4,5)) #sort by year then month then day then hour then minute and then by second
    joinedlist=[]
    for item in combinelist:
        year,month,day,hour,minute,sec,message,name,phone=item            #Breakes the sorted tuples down and assigns them variable names
        joinedtuple=(year+'-'+month+'-'+day, hour+':'+minute+':'+sec, message, name, phone) #Combines dates and times back into thier original format with colons and dashes
        joinedlist.append(joinedtuple)
    return joinedlist

#removes line/part of line if found in "invalid_msg_content" list
invalid_msg_content=["\x01","\x05","\n"]                        #A list of characters that followed right after text messages ###(Specification 3.0.1)###
def remove_nonmsg(line):
    if line[10]=='T':                                           #Some invalid messages had a capital T at index 10 so we got rid of those
        return
    for invalid in invalid_msg_content:                 
        if invalid in line:
            invalidloc=line.find(invalid)                       #Find the index number of the invalid message content
            line=line[:invalidloc]                              #Then we get rid of everything from that point on 
    return line

############################## caller name and phone number methods ############################## Specification 2.0.X
#checks for 7 or more digits in a row
def phonepatern(line):
   number=re.findall('\d{7,}',line)                             #Finds numbers that are at least seven digits in a row
   number=str(number)
   number=number[2:-2]                                          #Gets rid of some unwanted leading and trailing characters 
   return number
           
#returns caller name or None if no name is available
def getname(line, phone):
    if phone and line:
        first=phone[0]
        firstloc=line.find(first)                               #Finds the location of the first character in the phone number
        name=line[:firstloc]                                    #Removes the phone number leveing just the name
        if name=="":                                            
            name="None"                                         #Assigns the name of None to the person if not available in bin file
        return name
    
########################################## phone Details ########################################## Specification 3.0.1
#Phone details are found in the file in the format of "ro.product.brand=" for example. The following functions look for
#Those strings and gets the information right after the equal sign.

def phonedetails(finone):
    infolist=[]
    for line in finone:
        brand=product_brand(line)                               #Calls below function for the product brand
        model=product_model(line)                               #Calls below function for the product model
        host=build_host(line)                                   #Calls below function for the build host
        version=build_version(line)                             #Calls below function for the build version
        if brand is not None:
            infolist.append(brand)
        if model is not None:
            infolist.append(model)
        if host is not None:
            infolist.append(host)
        if version is not None:
            infolist.append(version)
    return infolist

#since lines can be found in bin file more than once we set the bellow booleans to true to get them to stop after finding it just once
brandfound=False
modelfound=False
hostfound=False
versionfound=False

#Gets the product brand
def product_brand(line):
    global brandfound
    brandstring='ro.product.brand='
    if brandstring in line and brandfound==False:
        brandfound=True
        loc=line.find(brandstring)
        outline='Product Brand: '+line[loc+len(brandstring):-1]
        return outline

#Gets the product model
def product_model(line):
    global modelfound
    modelstring='ro.product.model='
    if modelstring in line and modelfound==False:
        modelfound=True
        loc=line.find(modelstring)
        outline='Product Model: '+line[loc+len(modelstring):-1]
        return outline

#Gets the build host
def build_host(line):
    global hostfound
    hoststring="ro.build.host="
    if hoststring in line and hostfound==False:
        hostfound=True
        loc=line.find(hoststring)
        outline="Build Host: "+line[loc+len(hoststring):-1]
        return outline

#Gets the build version
def build_version(line):
    global versionfound
    versionstring='ro.build.version.release='
    if versionstring in line and versionfound==False:
        versionfound=True
        loc=line.find(versionstring)
        outline='Build Version: '+line[loc+len(versionstring):-1]
        return outline
