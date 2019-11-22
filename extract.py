#Manage Import
import datetime
import sqlite3
import re
import os.path

#Check the type of a value, if this is an image encapsulate with img tag
def checkType(val):
    html = ''
    val = str(val)
    regex = re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)",val)
    if (regex):
        html += '<a href="'+val+'" target="_blank" data-toggle="lightbox" data-footer="Source: '+val+'"><img src="'+val+'" class="img-fluid img-thumbnail"/></a>'
    else:
        html += val
        
    return html
    

#Show all data from a specific table
def showTableData(tableName):
    html = ''
    cursor.execute("SELECT * FROM "+tableName)
    data = cursor.fetchall()
    for row in data:
        html += '<tr>'
        for val in row:
            html += '<td>'+checkType(val)+'</td>'
        html += '</tr>'
    return html

#Show structure of a specific table
def showTableStructure(tableName):
    html = ''
    cursor.execute("PRAGMA table_info("+tableName+")")
    results = cursor.fetchall()
    for tab in results:
        html += '<td>'+tab[1]+'</td>' 
    return html
    

#Get all table name
def showTable(aList):
    html = ''
    for el in aList:
        html += '<h2 class="display-4">Table: <small class="text-muted">'+el[0]+'</small></h2><br/>'
        
        #Get structure first
        html += '''
        <div class="table-responsive">
        <table class="table table-striped table-bordered table-hover">
            <thead class="thead-dark">
                <tr>
        '''
        html += showTableStructure(el[0])
        html += '''
                </tr>
            </thead>
            <tbody>
        '''
        
        #Get All Data (after structure)
        html += showTableData(el[0])
        
        html += '''
            </tbody>
        </table>
        </div>
        <br/><br/>
        '''
        
    return html


#Construct report.html
def htmlGenerator(data):
    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = 'extract_'+ now +'.html'
    
    #Encoding character problem => https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
    with open(filename, "w", encoding="utf-8") as f:
    
        htmlStart = '''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <title>Extraction DB</title>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.css" integrity="sha256-HAaDW5o2+LelybUhfuk0Zh2Vdk8Y2W2UeKmbaXhalfA=" crossorigin="anonymous" />
        </head>
        <body class="bg-light">
            <div class="container">
                <h1 class="display-4">Extract BDD '''+now+'''</h1>
                <hr/>
        '''

        htmlContent = showTable(data)

        htmlEnd = '''
            </div>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.min.js" integrity="sha256-Y1rRlwTzT5K5hhCBfAFWABD4cU13QGuRN6P5apfWzVs=" crossorigin="anonymous"></script>
        <script>
        $(document).on('click', '[data-toggle="lightbox"]', function(event) {
                event.preventDefault();
                $(this).ekkoLightbox();
            });
        </script>
        </body>
        </html>
        '''

        html = htmlStart + htmlContent + htmlEnd
        f.write(html)
    f.close()
    
    return filename

#Start Script by asking where file is:
myFile = input('Path of DB file? ')

if (os.path.isfile(myFile)):
    print("Connecting DB...")
    #Start, connect to local DB
    connection = sqlite3.connect(myFile)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' ORDER BY name LIMIT 0,30")    

    #Launch file creation & print name
    print("File created: "+htmlGenerator(cursor.fetchall()))
else:
    print("Error: input is not a file!")