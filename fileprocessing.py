import os
import sys
import string
import operator

print_to_shell=True #once fixed a false will print output to a text document true to print to the python shell

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
print_to_shell=True
print_to_doc=False

def main():
    sys.setrecursionlimit(10000000)
    #so far just manually type in the read in file
    path="binfiles/mystery/mtd5_userdata.bin"
    fin=open(path,"rb")
            
    #List to store phone brands, carriers, and models found in bin to help find patterns 
    filelist=[]
    for line in fin:
        line=wantedchars(line)
        line=repr(line)
        filelist.append(line)

    #functions to find phone details
    print product_brand(filelist)
    print product_name(filelist)
    print build_host(filelist)
    print build_version(filelist)

############phone specific processes(brand, carrier, model)############

    ###mystery phone###
    for line in filelist:
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
                if msg.startswith(i):
                    if notdashdate(date)==True:
                        break
                    if faketime(time)==True:
                        break
                    if fakemsg(msg)==True:
                        break
                    if phone and name:
                        rtouple=(date, time, phone, name)
                    elif not phone:
                        rtouple=(date, time, msg)
                    if not msg.startswith(i):
                        outdata.append(rtouple)
                    elif msg.startswith(i):
                        date2=str(msg[0:10])
                        time2=str(msg[11:19])
                        msg2=str(msg[19:])
                        name2=getname(msg2, phone)
                        if notdashdate(date2)==True:
                            break
                        if faketime(time2)==True:
                            break
                        if fakemsg(msg2)==True:
                            break
                        if phone and name:
                            xltouple=(date, time, date2, time2, phone, name2)
                        elif not phone:
                            xltouple=(date, time, date2, time2, msg2)
                        if not msg2.startswith(i):
                            outdata.append(xltouple)
                        if msg2.startswith(i):
                            date3=str(msg2[0:10])
                            time3=str(msg2[11:19])
                            msg3=str(msg2[19:])
                            if notdashdate(date3)==True:
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
    printtuple()
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
    outdatasort=sortdata()
    combinedlist=combinedatetime(outdatasort)
    #alldata=callermatch(combinedlist)
    for line in combinedlist:
        if print_to_shell==True:
            print line
        if print_to_doc==True:
            fout=open(filename+'.txt','wb')
            print>>fout,line
            fout.close()
        
#sorts tuples by index number
def sortdata():
    outdatasep=[]
    for tup in outdata:
        if len(tup)==6:
            date1,time1,date2,time2,phone,name=tup
            date1=date1.split('-')
            time1=time1.split(':')
            date2=date2.split('-')
            time2=time2.split(':')
            newtup=(date1[0],date1[1],date1[2],time1[0],time1[1],time1[2],date2[0],date2[1],date2[2],time2[0],time2[1],time2[2],phone,name)
            outdatasep.append(newtup)
        if len(tup)==5:
            date1,time1,date2,time2,message=tup
            date1=date1.split('-')
            time1=time1.split(':')
            date2=date2.split('-')
            time2=time2.split(':')
            newtup=(date1[0],date1[1],date1[2],time1[0],time1[1],time1[2],date2[0],date2[1],date2[2],time2[0],time2[1],time2[2],message)
            outdatasep.append(newtup)
            
    outdatasort=sorted(outdatasep, key=operator.itemgetter(0,1,2,3,4,5))
    return outdatasort
def combinedatetime(tuplelist):
    combinelist=[]
    for tup in tuplelist:
        if len(tup)==14:
            year1,month1,day1,hour1,min1,sec1,year2,month2,day2,hour2,min2,sec2,phone,name=tup
            newtup=(year1+'-'+month1+'-'+day1,hour1+':'+min1+':'+sec1,year2+'-'+month2+'-'+day2,hour2+':'+min2+':'+sec2,phone,name)
            combinelist.append(newtup)
        if len(tup)==13:
            year1,month1,day1,hour1,min1,sec1,year2,month2,day2,hour2,min2,sec2,message=tup
            newtup=(year1+'-'+month1+'-'+day1,hour1+':'+min1+':'+sec1,year2+'-'+month2+'-'+day2,hour2+':'+min2+':'+sec2,message)
            combinelist.append(newtup)
    return combinelist

##def callermatch(tuplelist):
##    matchedlist=[]
##    tupcount=0
##    for tupline in tuplelist:
##        tupcount+=1
##        messageline=0
##        numberline=0
##        if len(tupline)==5:
##            messageline+=1
##            date1,time1,date2,time2,message=tup
##        if len(tupline)==6:
##            numberline+=1
##            date1,time1,date2,time2,phone,name=tup
##
##            newtup=date1,time1,date2,time2,phone,name,message
##            
##        else
##            matchedlist.append('error',tupline)
            
        
        
        
    #return matchedlist
        
    

#removes all but the standered chars               
def wantedchars(line):
    lineout=""
    for char in line:
        if ord(char)>=32 and ord(char)<=126:
            lineout+=char
    if lineout is not None:
        return lineout
    
##########phone specifics##########
def product_brand(filelist):
    for line in filelist:
        if "ro.product.brand=" in line:
            eq=line.find('=')
            return "Product Brand: "+line[eq+1:-1]
        
    return "Not Found"

def product_name(filelist):
    for line in filelist:
        if "ro.product.model=" in line:
            eq=line.find('=')
            return "Product Model: "+line[eq+1:-1]
        
    return "Not Found"

def build_host(filelist):
    for line in filelist:
        if "ro.build.host=" in line:
            eq=line.find('=')
            return "Build Host: "+line[eq+1:-1]
            
    return "Not Found"

def build_version(filelist):
    for line in filelist:
        if "ro.build.version.release=" in line:
            eq=line.find('=')
            return "Build Version: "+line[eq+1:-1]
        
    return "Not Found"

def phone_brand_search(filelist):
    acer_count=0
    amazon_count=0
    alcatel_count=0
    apple_count=0
    asus_count=0
    att_count=0
    blackberry_count=0
    cherry_count=0
    firefly_count=0
    garmin_count=0
    htc_count=0
    hp_count=0
    huawei_count=0
    lg_count=0
    motorola_count=0
    myphone_count=0
    nokia_count=0
    o2_count=0
    palm_count=0
    panasonic_count=0
    samsung_count=0
    sanyo_count=0
    siemens_count=0
    sonim_count=0
    sony_count=0
    tmobile_count=0
    verizon_count=0
    brandlist={'Acer':acer_count,'Amazon':amazon_count,'Alcatel':alcatel_count,'Apple':apple_count,'Asus':asus_count,'AT&T':att_count,
               'Blackberry':blackberry_count,'Cherry mobile':cherry_count,'Firefly':firefly_count,'Garmin':garmin_count,
               'HTC':htc_count,'Hewlett-Packard':hp_count,'Huawei':huawei_count,'LG':lg_count,'Motorola':motorola_count,
               'MyPhone':myphone_count,'Nokia':nokia_count,' O2 ':o2_count,'Palm':palm_count,'Panasonic':panasonic_count,
               'Samsung':samsung_count,'Sanyo':sanyo_count,'Siemens':siemens_count,'Sonim':sonim_count,'Sony':sony_count,
               'T-mobile':tmobile_count,'Verizon':verizon_count}
    
    for line in filelist:
        for brand, count in brandlist.items():
            if brand in line:
                brandlist[brand]=count+1

    for brand, count in brandlist.iteritems():
        if count>0:
            print "Possible Brand: "+str(brand)+" found "+str(count)+" times."
        

def phone_os_search(filelist):
    android_count=0
    bada_count=0
    blackberry_count=0
    ios_count=0
    mobile_linux_count=0
    windows_ce_count=0
    windows_mobile_count=0
    windows_phone_count=0
    oslist={'Android':android_count,'BADA':bada_count,'BlackBerry':blackberry_count,
            'IOS':ios_count,'Mobil Linux':mobile_linux_count,'Windows CE':windows_ce_count,
            'Windows Mobile':windows_mobile_count,'Windows Phone':windows_phone_count}
    
    for line in filelist:
        for os, count in oslist.items():
            if os in line:
                oslist[os]=count+1

    for os, count in oslist.iteritems():
        if count>0:
            print "Possible OS: "+str(os)+" found "+str(count)+" times."
        
    
def carrier_name_search(filelist):
    verizon_count=0
    att_count=0
    sprint_count=0
    tmobile_count=0
    tracfone_count=0
    metropcs_count=0
    circket_count=0
    us_count=0
    carriers={'Verizon Wireless':verizon_count,'AT&T Mobility':att_count,'Sprint Nextel':sprint_count,
              'T-Mobile USA':tmobile_count,'TracFone Wireless':tracfone_count,'MetroPCS':metropcs_count,
              'Cricket Wireless':circket_count,'U.S. Cellular':us_count}
    
    for line in filelist:
        for car, count in carriers.items():
            if car in line:
                carriers[car]=count+1

    for car, count in carriers.iteritems():
        if count>0:
            print "Possible Carrier: "+str(car)+" found "+str(count)+" times."
    
def model_number_search(filelist):
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
def notdashdate(line):
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
def phonepatern(line):#note: a fix is needed for phone numbers without the area code, currently they are caught as text messages
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

