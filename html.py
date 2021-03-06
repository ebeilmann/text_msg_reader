

##### Making HTML file ##### Specification 7.0.X - 10.0.X
# example input: input = [('Date','Time','Message','Name','Phone Number'),('Date','Time','Message','Name','Phone Number'),('Date','Time','Message','Name','Phone Number')]

#The below code takes all the information from the list of tuples we gave it and puts it into an html table
def createOutputFile(phoneinfo, input):
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
        '<tr>\n'
        '<td style="width: 130px; background: #000000;" colspan="5"><h3>' + phoneinfo[0] + '</h3></td>\n'
        '</tr>\n'
        '</table>\n' 
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
        f.write('<td><p>c</p></td>')
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
