import os
import sys
import string
import operator
import re

print_to_doc=False 
print_to_shell=False
make_html=True
def main():
    
    # validate command line arguments # specification 1.0.X
    if len(sys.argv) != 2:
        fail()
    if not os.path.isfile(sys.argv[1]):
        fail()
    path=sys.argv[1]
    filename=os.path.basename(path)
    basename=os.path.basename(path)
    dotloc=basename.find(".")
    basename=basename[:dotloc]
    finone=open(path,'rb')
    fintwo=open(path,'rb')

    #starts with fresh document to write too since future data will be appended
    if print_to_doc==True:
        clearfile=open(basename+'.txt','w')
        clearfile.close()
    
    years=['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013']
    predata=[]
    outdata=[]
    #functions to find phone details
    phoneinfolist=phonedetails(finone) # specification 3.0.1
    outdata.append(phoneinfolist)
    
    splitfilelist=[]
    for line in fintwo:
        for year in years:
            yearcount=line.count(year+'-')
            while yearcount>1:
                lastyearloc=line.rfind(year+'-')
                newline=line[lastyearloc:]
                line=line[:lastyearloc]
                yearcount=line.count(year+'-')
                newline=remove_nonmsg(newline) # specification 3.0.2
                if newline is not None:
                    splitfilelist.append(newline)

    for line in splitfilelist:
        date=str(line[0:10]) # specification 4.0.1
        time=str(line[11:19]) # specification 4.0.1
        msg=str(line[19:]) # specification 5.0.1
        msg.replace("  "," ")
        phone=""
        name=""
        phonepos=phonepatern(msg) # Specification 2.0.X
        if phonepos is not None:
            phone=phonepos
        name=getname(msg, phone)
        if len(phone)==20:
            half=len(phone)/2
            phone=phone[:half]
        if phone and name:
            texttuple=(date, time, phone, name)
            predata.append(texttuple)
        else:
            texttuple=(date, time, msg)
            if msg is not None:
                predata.append(texttuple)
                
    sorteddata=sortdata(predata) # specification 5.0.1
    print len(sorteddata)
    outdata.append(sorteddata)
    phoneinfo=outdata[0]
    textinfo=outdata[1]
    if print_to_shell==True: #for printing to shell
        for line in phoneinfo:
            print line
        for line in textinfo:
            print line
    if print_to_doc==True: #for printing to a text file
        fout=open(basename+'.txt','a')
        for line in phoneinfo:
            print>>fout,line
        for line in textinfo:
            print>>fout,line
        fout.close()
    if make_html==True:
        createOutputFile(textinfo) #for printing to an html file # Specification 7.0.X - 10.0.X
    finone.close()
    fintwo.close()
    
################################# process text message methods ################################# Specification Optional
#sorts tuples by date and time then matches callers and their phone numbers to the text messages
def sortdata(filelist): # Specification optional
    msgdata=[]
    numdata=[]
    #Breaks up tuples for easy sorting and matching of text with caller(rejoined together further down)
    for tup in filelist:
        if len(tup)==4:
            date,time,phone,name=tup           
            sdate=date.split('-')
            stime=time.split(':')
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],phone,name)
                numdata.append(newtup)
        if len(tup)==3:
            date,time,message=tup
            sdate=date.split('-')
            stime=time.split(':')
            if len(sdate)==3 and len(stime)==3:
                newtup=(sdate[0],sdate[1],sdate[2],stime[0],stime[1],stime[2],message)
                msgdata.append(newtup)
                
    #Combines text messages with the caller and phone number           
    combinelist=[]
    for msg in msgdata:
        for num in numdata:
            year=''
            month=''
            day=''
            hour=''
            minute=''
            sec=''
            phone=''
            name=''
            message=''
            numyear,nummonth,numday,numhour,nummin,numsec,phone,name=num
            msgyear,msgmonth,msgday,msghour,msgmin,msgsec,message=msg
            if numyear==msgyear:
                year=msgyear
            if nummonth==msgmonth:
                month=msgmonth
            if numday==msgday:
                day=msgday
            if numhour==msghour:
                hour=msghour
            if nummin==msgmin:
                minute=msgmin
            if int(numsec)+1>int(msgsec) and int(numsec)-1<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+2>int(msgsec) and int(numsec)-2<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+3>int(msgsec) and int(numsec)-3<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+4>int(msgsec) and int(numsec)-4<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+5>int(msgsec) and int(numsec)-5<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+6>int(msgsec) and int(numsec)-6<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+7>int(msgsec) and int(numsec)-7<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+8>int(msgsec) and int(numsec)-8<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+9>int(msgsec) and int(numsec)-9<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+10>int(msgsec) and int(numsec)-10<int(msgsec):
                sec=str(msgsec)
            elif int(numsec)+11>int(msgsec) and int(numsec)-11<int(msgsec):
                sec=str(msgsec)
            if year!='' and month!='' and day!='' and hour!='' and minute!='' and sec!='':
                combinetuple=(year,month,day,hour,minute,sec,message,name,phone)
                combinelist.append(combinetuple)

    #sort by year, month, day, hour, minute, and second
    combinelist=sorted(combinelist, key=operator.itemgetter(0,1,2,3,4,5))
    #Rejoin all data back into a tuple with original time and date format
    joinedlist=[]
    for item in combinelist:
        year,month,day,hour,minute,sec,message,name,phone=item
        joinedtuple=(year+'-'+month+'-'+day, hour+':'+minute+':'+sec, message, name, phone)
        joinedlist.append(joinedtuple)
    return joinedlist

#removes line/part of line if found in "invalid_msg_content" list
invalid_msg_content=["\x01","\x05","\n"] # Specification 3.0.1
def remove_nonmsg(line):
    if line[10]=='T':
        return
    for invalid in invalid_msg_content:
        if invalid in line:
            invalidloc=line.find(invalid)
            line=line[:invalidloc]
    return line

############################## caller name and phone number methods ############################## Specification 2.0.X
#checks for 7 or more digits in a row
def phonepatern(line):
   number=re.findall('\d{7,}',line)
   number=str(number)
   number=number[2:-2]
   return number
           
#returns caller name or None if no name is available
def getname(line, phone):
    if phone and line:
        first=phone[0]
        firstloc=line.find(first)
        name=line[:firstloc]
        if name=="":
            name="None"
        return name
    
########################################## phone Details ########################################## Specification 3.0.1
def phonedetails(finone):
    infolist=[]
    for line in finone:
        brand=product_brand(line)
        model=product_model(line)
        host=build_host(line)
        version=build_version(line)
        if brand is not None:
            infolist.append(brand)
        if model is not None:
            infolist.append(model)
        if host is not None:
            infolist.append(host)
        if version is not None:
            infolist.append(version)
    return infolist

brandfound=False
modelfound=False
hostfound=False
versionfound=False

def product_brand(line):
    global brandfound
    brandstring='ro.product.brand='
    if brandstring in line and brandfound==False:
        brandfound=True
        loc=line.find(brandstring)
        outline='Product Brand: '+line[loc+len(brandstring):-1]
        return outline

def product_model(line):
    global modelfound
    modelstring='ro.product.model='
    if modelstring in line and modelfound==False:
        modelfound=True
        loc=line.find(modelstring)
        outline='Product Model: '+line[loc+len(modelstring):-1]
        return outline

def build_host(line):
    global hostfound
    hoststring="ro.build.host="
    if hoststring in line and hostfound==False:
        hostfound=True
        loc=line.find(hoststring)
        outline="Build Host: "+line[loc+len(hoststring):-1]
        return outline

def build_version(line):
    global versionfound
    versionstring='ro.build.version.release='
    if versionstring in line and versionfound==False:
        versionfound=True
        loc=line.find(versionstring)
        outline='Build Version: '+line[loc+len(versionstring):-1]
        return outline

#################################### Making HTML file #################################### Specification 7.0.X - 10.0.X
# example input: input = [('Date','Time','Message','Name','Phone Number'),('Date','Time','Message','Name','Phone Number'),('Date','Time','Message','Name','Phone Number')]

# Specification 7.0.X - 10.0.X
def createOutputFile(input):
    detailnum=4
    f = open('output.html', 'w+')
    f.close()    
    f = open('output.html', 'w')
    f.write('<!DOCTYPE html>\n'
        '<html>\n'
        '<head>\n'
        '<title>Text Message Reader</title>\n'
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
        '<style>'
            'body {height:100%; margin: 0; padding: 0; font-family: arial, verdana, tahoma, sans-serif;}'
            'html {height:100%; margin: 0; padding: 0; font-family: arial, verdana, tahoma, sans-serif;}'
            'p { font-size: 10pt; margin: 0; padding: 3px;}'
            'h3 { color: #f0f0f0; font-size: 12pt; margin: 0; padding: 2px;}'
            'table { width: 100%; border-width: 0px;}'
            '#header { background: #333333;}'
            '#odd { background: #f9f9f9;}'
            '#even { background: #d5e0e4;}'
        '</style>\n'
        '</head>\n'
        '<body>\n'
        '<table>\n'
        '<tr id="header">\n'
        '<td style="width: 130px;"><h3>Date:</h3></td>\n'
        '<td style="width: 130px;"><h3>Time:</h3></td>\n'
        '<td style="width: 280px;"><h3>Message:</h3></td>\n'
        '<td style="width: 130px;"><h3>Name:</h3></td>\n'
        '<td style="width: 130px;"><h3>Phone Number:</h3></td>\n'
        '</tr>\n')

    for i in range(0, len(input)-1,2):
        f.write('<tr id="odd"><td><p>' + input[i][0] + '</p></td>\n')
        f.write('<td><p>' + input[i][1] + '</p></td>')
        f.write('<td><p>' + input[i][2] + '</p></td>')
        f.write('<td><p>' + input[i][3] + '</p></td>')
        f.write('<td><p>' + input[i][4] + '</p></td></tr>')

        f.write('<tr id="even"><td><p>' + input[i+1][0] + '</p></td>\n')
        f.write('<td><p>' + input[i+1][1] + '</p></td>')
        f.write('<td><p>' + input[i+1][2] + '</p></td>')
        f.write('<td><p>' + input[i+1][3] + '</p></td>')
        f.write('<td><p>' + input[i+1][4] + '</p></td></tr>')
        
    f.write('</table></body></html>\n')
    f.close()

def fail():
    print "Missing or invalid argument."
    print "Please enter the name of a '.bin' file."
    print "Examples of usage:"
    print "phonesearch.py nokia.bin"
    print "If the path has a space, use quotation marks."
    print '"phone search.py"'
    sys.exit(-1)
    
main()

