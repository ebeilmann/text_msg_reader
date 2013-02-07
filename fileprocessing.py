import os
import sys
import string
import operator

print_to_shell=True #false for print to a text document true to print to shell

years=['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013']

#some key strings i was thinking we could use to eliminate unnecisary lines
#I found these strings in lines that contained no text messages and
#I think no text message lines contained these strings
invalid_msg_content=['<title>','<updated>','>Updated','<catagory ','uploaded>','http','div>','span>',
                     'Metadata','@gmail.com','</date>','UTC','ModifyDate','CreateDate>','meta>',
                     'htc.android.pcs','ApplicationWillTerminateNotification','date:modify']

valid_date_dash=['0','1','2','3','4','5','6','7','8','9','-']
valid_time=['0','1','2','3','4','5','6','7','8','9',':']

phone=''
outdata=[]

android=False
verizon=False

def main():
    sys.setrecursionlimit(10000000)
    fin=open("moto-verizon.bin","rb")#so far just manually type in the read in file
            
    #List to store phone brands, carriers, and models found in bin to help find patterns 
    foundbrands=[]
    foundcarriers=[]
    foundmodels=[] 
    for line in fin:
        line=wantedchars(line)
        line=repr(line)

        #was going to use this to remove all deuplicate lines
        #filelist=duplicateremoval(filelist)

        #functions to find phone details - didn't finish yet
        #phonebrand(filelist)
        #carriername(filelist)
        #modelnumber(filelist)

############phone specific processes(brand, carrier, model)############
        
        ###verizon, motorola, W385###
        #these bools are just hardcoded for now to be changed later so that the program will set them
        #when we get the brand, carrier and file recognition methods to work
        #verizon=True
        #motorola=True
        #W385=True
        #
        #some work i was doing - so far just I am just trying to recognize paterns assosiated
        #with text message lines
        #this was working somewhat before i transfered it over into this file also
        #I'll work on it
        #if  verizon==True and motorola==True and W385==True:
        if fin=="moto-verizon.bin":
            print line
            if line.startswith('From'):
                print line
            elif line.startswith('7'):
                print line
            elif line.startswith(':'):
                print line
            elif line.startswith('A'):
                print line
            elif line.startswith('$'):
                print line
            elif line.startswith('+'):
                print line
            elif line.startswith('9'):
                print line
            else:
                phonepatern(line)

                
        ###mystery phone###
        #some work i was doing - this gives pretty good results even if some results are not text messages
        #transfering it over to this file seems to have messed some things up
        #fileprocessing_mtd5.py is the file I tansfered it from
        #
        #Before transfering it over it gave almost 200 lines now it only gives about 100 lines
        #
        #The multiple "if msg.startswith(i):" statements was for the lines that contained multiple dates and
        #times. It is one of the things that used to work but not anymore.
        mystery=False
        if mystery==True:
            for i in years:
                if i in line:
                    while not line.startswith(i):
                        line=line[1:]
                    date=str(line[0:10])
                    time=str(line[11:19])
                    msg=str(line[19:])
                    phone=""
                    phonepos=phonepatern(msg)
                    if phonepos is not None:
                        phone+=phonepos
                    name=getname(msg, phone)
                    if not msg.startswith(i):
                        if dashdate(date)==True:
                            break
                        if faketime(time)==True:
                            break
                        if fakemsg(msg)==True:
                            break
                        if phone and name:
                            rtouple=(date, time, phone, name)
                        elif not phone:
                            rtouple=(date, time, msg)
                        print rtouple
                        outdata.append(rtouple)
                    if msg.startswith(i):
                        date2=str(msg[0:10])
                        time2=str(msg[11:19])
                        msg2=str(msg[19:])
                        name2=getname(msg2, phone)
                        if not msg.startswith(i):
                            if dashdate(date)==True:
                                break
                            if faketime(time)==True:
                                break
                            if dashdate(date2)==True:
                                break
                            if faketime(time2)==True:
                                break
                            if fakemsg(msg2)==True:
                                break
                            if phone and name:
                                xltouple=(date, time, date2, time2, phone, name2)
                            elif not phone:
                                xltouple=(date, time, date2, time2, msg2)
                            outdata.append(xltouple)
                            print xltouple
                        if msg2.startswith(i):
                            date3=str(msg2[0:10])
                            time3=str(msg2[11:19])
                            msg3=str(msg2[19:])
                            if dashdate(date)==True:
                                break
                            if faketime(time)==True:
                                break
                            if dashdate(date2)==True:
                                break
                            if faketime(time2)==True:
                                break
                            if dashdate(date3)==True:
                                break
                            if faketime(time3)==True:
                                break
                            if fakemsg(msg3)==True:
                                break
                            name3=getname(msg3, phone)
                            if phone:
                                xxltouple=(date, time, date2, time2, date3, time3, phone, name3)
                            elif not phone:
                                xxltouple=(date, time, date2, time2, date3, time3, msg3)
                            outdata.append(xxltouple)
                            print xxltouple
    fin.close()


            
##########process and print methods##########    
def duplicateremoval(filelist):
    dupfree=[]
    for line in range(len(filelist)):
        for item in range(len(filelist)):
            #print 'test1', line, filelist[line]
            #print 'test2', item, filelist[item]
            if filelist[line] == filelist[item] and line!=item:
                filelist[item]=''
                #print 'none',filelist[item]
    for part in filelist:
        if part is '':
            break
        else:
            dupfree.append(part)
    return dupfree

def printtuple():
    for item in outdata:
        if print_to_shell==True:
            print item
        else:
            fout=open(filename+'.txt','wb')
            print>>fout,item
            fout.close()
        
#sorts tuples by index number
def sortdata():
    index=0
    self.outdata.sort(key=operator.itemgetter(index))

#removes all but the standered chars               
def wantedchars(line):
    lineout=""
    for char in line:
        if ord(char)>=32 and ord(char)<=126:
            lineout+=char
    if lineout is not None:
        return lineout
    
##########phone specifics##########     
def phonebrand(filelist):
    brands=['Apple','Firefly','Garmin','Motorola','Palm','Sanyo','Sonim','Sony']
    foundbrands=[]
    for brand in brands:
        for line in filelist:
            if brand in line:
                foundbrands.append(brand)
    if len(foundbrands)>=1:
        for item in foundbrands:
            print 'Found Brand: ',item
    else:
        print 'unknown phone type'

    
def carriername(filelist):
    carriers=['Verizon Wireless','AT&T Mobility','Sprint Nextel','T-Mobile USA','TracFone Wireless','MetroPCS','Cricket Wireless','U.S. Cellular']
    foundcarriers=[]
    for carrier in carriers:
        for line in filelist:
            if carrier in line:
                foundcarriers.append(carrier)
    if len(foundcarriers)>=1:
        for item in foundcarriers:
            print 'Found Carrier: ',item
    else:
        print 'unknown carrier'
    
def modelnumber(filelist):
    models=['Motorola W385']
    foundmodels=[]
    for model in models:
        for line in filelist:
            if model in line:
                foundmodelss.append(model)
    if len(foundmodels)>=1:
        for item in foundmodels:
            print 'Found Model: ',item
    else:
        print 'unknown model'
        
##########date methods##########
#cuts out everything before the year
#for use with phones that display date before other data with year first
def datefinder(line, date):
    while not line.startswith(date):
        line=line[1:]
    return line

#for dates formated with dashes
def dashdate(line):
    global valid_date_dash
    errorcount=0
    dashcount=0
    for i in range(len(line)):
        if line[i] not in valid_date_dash:
            errorcount+=1
        if errorcount>0:
            return True
        if line[i] in '-':
            dashcount+=1
    if dashcount<2:
        return True
    return False

##########time methods##########
def faketime(line):
    global valid_time
    errorcount=0
    coloncount=0
    for i in range(len(line)):
        if line[i] not in valid_time:
            errorcount+=1
        if errorcount>0:
            return True
        if line[i] in ':':
            coloncount+=1
    if coloncount<2:
        return True
    else:
        return False

##########text message methods##########
#removes line if found in "invalid_msg_content" list
def fakemsg(line):
    let_num_count=0
    errorcount=0
    if line.isspace():
        return True
    if len(line)>1000:
        return True
    for i in invalid_msg_content:
        if i in line:
            return True
    for i in range(len(line)):
        if line[i].isalnum():
            let_num_count+=1
    if let_num_count<1:
        return True
    return False

##########phone number methods##########
#checks for 10 digits in a row 
def phonepatern(line):
    number=''
    for char in line:
        if len(number)==10:
            return number
        if ord(char)>=48 and ord(char)<=57:
            number+=char
        else:
            number=''
            
##########caller name methods##########
#returns caller name    
def getname(line, phone):
    if phone and line:
        first=phone[0]
        firstloc=line.find(first)
        name=line[:firstloc]
        return name
    
main()

