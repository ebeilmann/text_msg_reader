import os
import sys
import string
import operator
import re

################################# Process text message methods ################################# Specification Optional
#Sorts tuples by date and time then matches callers and their phone numbers to the text messages
def sortdata(filelist): # Specification optional
    msgdata=[]
    numdata=[]
    #Breaks up tuples for easy sorting and matching of text with caller(rejoined together further down)
    for tup in filelist:
        if len(tup)==4:
            date,time,phone,name=tup                                #Splits up the tuple
            sdate=date.split('-')                                   #Splits the date into three different numbers
            stime=time.split(':')                                   #Splits time into three different numbers
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],phone,name)
                numdata.append(newtup)                              #Repacks the tuples with the now separated dates and times
        if len(tup)==3:
            date,time,message=tup                                   #Splits up the tuple
            sdate=date.split('-')                                    #Splits the date into three different numbers
            stime=time.split(':')                                   #Splits time into three different numbers
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],message)
                msgdata.append(newtup)                              #Repacks the tuples with the now separated dates and times

    msgdata=sorted(msgdata, key=operator.itemgetter(0,1,2,3,4,5))   #Working with sorted data seems to speed up processing
    numdata=sorted(numdata, key=operator.itemgetter(0,1,2,3,4,5))
    
    #Combines text messages with the caller and phone number
    combinelist=[]
    for msg in msgdata:                                             #For every tuple in the list with text messages
        for num in numdata:                                         #For every tuple in the list with numbers and names
            year=''                                                 #Initialize each part of final tuple to nothing 
            month=''
            day=''
            hour=''
            minute=''
            sec=''
            phone=''
            name=''
            message=''
            numyear,nummonth,numday,numhour,nummin,numsec,phone,name=num #Breaks tuples down to more easily to compare values
            msgyear,msgmonth,msgday,msghour,msgmin,msgsec,message=msg

            if numyear==msgyear and nummonth==msgmonth and numday==msgday and numhour==msghour and nummin==msgmin:
                year=msgyear
                month=msgmonth
                hour=msghour
                day=msgday
                minute=msgmin
                if int(numsec)+10>int(msgsec) and int(numsec)-10<int(msgsec): #If all of the date and time values match within 10 seconds continue
                    sec=str(msgsec)
                    combinetuple=(year,month,day,hour,minute,sec,message,name,phone)#The data gets put back into a tuple
                    combinelist.append(combinetuple)                                #Then added to a list

    #Adds the dashes and colons back between the date and times
    combinelist=sorted(combinelist, key=operator.itemgetter(0,1,2,3,4,5)) #Sort by year then month then day then hour then minute and then by second
    joinedlist=[]
    for item in combinelist:
        year,month,day,hour,minute,sec,message,name,phone=item      #Breaks the sorted tuples down and assigns them variable names
        joinedtuple=(year+'-'+month+'-'+day, hour+':'+minute+':'+sec, message, name, phone) #Combines dates and times back into their original format with colons and dashes
        joinedlist.append(joinedtuple)
    return joinedlist

#removes line/part of line if found in "invalid_msg_content" list
invalid_msg_content=["\x01","\x05","\n"]                            #A list of characters that followed right after text messages ###(Specification 3.0.1)###
def remove_nonmsg(line):
    if line[10]=='T':                                               #Some invalid messages had a capital T at index 10 so we got rid of those
        return
    for invalid in invalid_msg_content:                 
        if invalid in line:
            invalidloc=line.find(invalid)                           #Find the index number of the invalid message content
            line=line[:invalidloc]                                  #Then we get rid of everything from that point on 
    return line

############################## caller name and phone number methods ############################## Specification 2.0.X
#checks for 7 or more digits in a row
def phonepatern(line):
   number=re.findall('\d{7,}',line)                                 #Finds numbers that are at least seven digits in a row
   number=str(number)
   number=number[2:-2]                                              #Gets rid of some unwanted leading and trailing characters 
   return number
           
#returns caller name or None if no name is available
def getname(line, phone):
    if phone and line:
        first=phone[0]
        firstloc=line.find(first)                                   #Finds the location of the first character in the phone number
        name=line[:firstloc]                                        #Removes the phone number leveing just the name
        if name=="":                                            
            name="None"                                             #Assigns the name of None to the person if not available in bin file
        return name
    
########################################## phone Details ########################################## Specification 3.0.1
#Phone details are found in the file in the format of "ro.product.brand=" for example. The following functions look for
#Those strings and gets the information right after the equal sign.
def phonedetails(finone):
    infolist=[]
    for line in finone:
        serial_number_var=serial_number(line)

        build_id_var=build_id(line)
        build_display_id_var=build_display_id(line)
        build_version_incremental_var=build_version_incremental(line)
        build_version_sdk_var=build_version_sdk(line)
        build_version_codename_var=build_version_codename(line)
        build_version_release_var=build_version_release(line)
        build_date_var=build_date(line)
        build_date_utc_var=build_date_utc(line)
        build_type_var=build_type(line)
        build_user_var=build_user(line)
        build_host_var=build_host(line)
        build_tags_var=build_tags(line)

        product_model_var=product_model(line)
        product_brand_var=product_brand(line)
        product_name_var=product_name(line)
        product_device_var=product_device(line)
        product_board_var=product_board(line)
        product_cpu_abi_var=product_cpu_abi(line)
        product_cpu_abi2_var=product_cpu_abi2(line)
        product_manufacturer_var=product_manufacturer(line)
        varlist=[serial_number_var, build_id_var, build_display_id_var, build_version_incremental_var, build_version_sdk_var,
                 build_version_codename_var, build_version_release_var, build_date_var, build_date_utc_var, build_type_var,
                 build_user_var, build_host_var, build_tags_var, product_model_var, product_brand_var, product_name_var,
                 product_device_var, product_board_var, product_cpu_abi_var, product_cpu_abi2_var, product_manufacturer_var]
        
        #Some checks to get rid of "None" values and duplicates
        for var in varlist:
            if var:
                infolist.append(var)
                if var==product_manufacturer_var:
                    return infolist

#Since lines can be found in bin file more than once we set the below
#Booleans to true to get them to stop after finding it just once
serial_number_found=False

build_id_found=False
build_display_id_found=False
build_version_incremental_found=False
build_version_sdk_found=False
build_version_codename_found=False
build_version_release_found=False
build_date_found=False
build_date_utc_found=False
build_type_found=False
build_user_found=False
build_host_found=False
build_tags_found=False

product_model_found=False
product_brand_found=False
product_name_found=False
product_device_found=False
product_board_found=False
product_cpu_abi_found=False
product_cpu_abi2_found=False
product_manufacturer_found=False

#All below functions work the same. They search for the exact
#String in the file that indicates the needed phone data
def serial_number(line):
    global serial_number_found
    outline=None
    string='androidboot.serialno='
    if string in line and serial_number_found==False:
        serial_number_found=True
        startloc=line.find(string)
        newline=line[startloc+len(string):-1]
        endloc=newline.find(" ")
        outline='Serial Number: '+newline[:endloc]
        return outline

#Build Information
def build_id(line):
    global build_id_found
    string='ro.build.id='
    if string in line and build_id_found==False:
        build_id_found=True
        loc=line.find(string)
        outline='Build ID: '+line[loc+len(string):-1]
        return outline

def build_display_id(line):
    global build_display_id_found
    string='ro.build.display.id='
    if string in line and build_display_id_found==False:
        build_display_id_found=True
        loc=line.find(string)
        outline='Build Display ID: '+line[loc+len(string):-1]
        return outline

def build_version_incremental(line):
    global build_version_incremental_found
    string='ro.build.version.incremental='
    if string in line and build_version_incremental_found==False:
        build_version_incremental_found=True
        loc=line.find(string)
        outline='Build Version Incremental: '+line[loc+len(string):-1]
        return outline

def build_version_sdk(line):
    global build_version_sdk_found
    string='ro.build.version.sdk='
    if string in line and build_version_sdk_found==False:
        build_version_sdk_found=True
        loc=line.find(string)
        outline='Build Version SDK: '+line[loc+len(string):-1]
        return outline

def build_version_codename(line):
    global build_version_codename_found
    string='ro.build.version.codename='
    if string in line and build_version_codename_found==False:
        build_version_codename_found=True
        loc=line.find(string)
        outline='Build Version Codename: '+line[loc+len(string):-1]
        return outline

def build_version_release(line):
    global build_version_release_found
    string='ro.build.version.release='
    if string in line and build_version_release_found==False:
        build_version_release_found=True
        loc=line.find(string)
        outline='Build Version Release: '+line[loc+len(string):-1]
        return outline

def build_date(line):
    global build_date_found
    string='ro.build.date='
    if string in line and build_date_found==False:
        build_date_found=True
        loc=line.find(string)
        outline='Build Date: '+line[loc+len(string):-1]
        return outline
    
def build_date_utc(line):
    global build_date_utc_found
    string='ro.build.date.utc='
    if string in line and build_date_utc_found==False:
        build_date_utc_found=True
        loc=line.find(string)
        outline='Build Date UTC: '+line[loc+len(string):-1]
        return outline


def build_type(line):
    global build_type_found
    string='ro.build.type='
    if string in line and build_date_utc_found==False:
        build_type_found=True
        loc=line.find(string)
        outline='Build Type: '+line[loc+len(string):-1]
        return outline

def build_user(line):
    global build_user_found
    string='ro.build.user='
    if string in line and build_user_found==False:
        build_date_utc_found=True
        loc=line.find(string)
        outline='Build User: '+line[loc+len(string):-1]
        return outline

def build_host(line):
    global build_host_found
    string="ro.build.host="
    if string in line and build_host_found==False:
        build_host_found=True
        loc=line.find(string)
        outline="Build Host: "+line[loc+len(string):-1]
        return outline

def build_tags(line):
    global build_tags_found
    string='ro.build.tags='
    if string in line and build_tags_found==False:
        build_tags_found=True
        loc=line.find(string)
        outline='Build Tags: '+line[loc+len(string):-1]
        return outline
    
#Product Information    
def product_model(line):
    global product_model_found
    string='ro.product.model='
    if string in line and product_model_found==False:
        product_model_found=True
        loc=line.find(string)
        outline='Product Model: '+line[loc+len(string):-1]
        return outline
    
def product_brand(line):
    global product_brand_found
    string='ro.product.brand='
    if string in line and product_brand_found==False:
        product_brand_found=True
        loc=line.find(string)
        outline='Product Brand: '+line[loc+len(string):-1]
        return outline

def product_name(line):
    global product_name_found
    string='ro.product.name='
    if string in line and product_name_found==False:
        product_name_found=True
        loc=line.find(string)
        outline='Product Name: '+line[loc+len(string):-1]
        return outline

def product_device(line):
    global product_device_found
    string='ro.product.device='
    if string in line and product_device_found==False:
        product_device_found=True
        loc=line.find(string)
        outline='Product Device: '+line[loc+len(string):-1]
        return outline
    
def product_board(line):
    global product_board_found
    string='ro.product.board='
    if string in line and product_board_found==False:
        product_board_found=True
        loc=line.find(string)
        outline='Product Board: '+line[loc+len(string):-1]
        return outline

def product_cpu_abi(line):
    global product_cpu_abi_found
    string='ro.product.cpu.abi='
    if string in line and product_cpu_abi_found==False:
        product_cpu_abi_found=True
        loc=line.find(string)
        outline='Product CPU ABI: '+line[loc+len(string):-1]
        return outline

def product_cpu_abi2(line):
    global product_cpu_abi2_found
    string='ro.product.cpu.abi2='
    if string in line and product_cpu_abi2_found==False:
        product_cpu_abi2_found=True
        loc=line.find(string)
        outline='Product CPU ABI2: '+line[loc+len(string):-1]
        return outline
    
def product_manufacturer(line):
    global product_manufacturer_found
    string='ro.product.manufacturer='
    if string in line and product_manufacturer_found==False:
        product_manufacturer_found=True
        loc=line.find(string)
        outline='Product Manufacturer: '+line[loc+len(string):-1]
        return outline
