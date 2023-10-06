from urllib.request import urlopen
from time import time
from datetime import datetime

#import logging
import getopt
import sys
import smtplib
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# check input arguments
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
options = "d:"
longOptions = ["Dir"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, longOptions)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-d", "--Dir"):
            print ("Setting base directory to " + currentValue + "\r\n")
            appBase = currentValue

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


####### App config
#env = 'prod'
env = 'dev'
# change sendEmail to True and add your smtp server to start sending email alerts
sendEmail = False
smtpHost = 'localhost'
mailFrom = 'Alerts`@noreply.com'
if env == 'prod':
  degradeMail = ['me@mail.com']
  outageMail = ['me@mail.com']
  baseDir = '/app/'
else:
  # set5 env to anything but prod for testing using the below values
  degradeMail = ['me@mail.com']
  outageMail = ['me@mail.com']
  baseDir = './'

replyTo = 'me@mail.com'

# if any page takes longer than duration_threshold seconds to load, performance will be considered degraded
durationThreshold = 10
########

if not appBase:
  appBase = baseDir

statusPage = appBase + 'site_monitor/status.html'


def url_check():
  try:
    response = urlopen(url)
  except Exception as e:
    #print e.reason
    duration = ''
    #else:
  else:
    response.read()
    endTime = time()
    duration = (round(endTime-startTime, 3))
  return duration

listFileName = appBase + 'site_monitor/urllist.txt'
statusRows = ""
divider = ""
with open(listFileName) as urlFile:
  print ("Checking URLs listed in " + listFileName + "\r\n")
  line = urlFile.readline()
  while line:
    # skip any lines in the input file that are commented
    if line[0][0] != '#':
      strippedLine = line.strip()
      app,url = strippedLine.rsplit(" ",1)
      startTime = time()
      sysTime = datetime.now()
      curTime = sysTime.strftime('%m-%d-%Y %H:%M:%S')
      #formatted_time = systime.strftime('%-I:%M:%S %p on %b %-d, %Y  ')
      formattedTime = sysTime.strftime('%H:%M:%S %p on %b , %Y  ')
      try:
        response = urlopen(url)
      except Exception as e:
        #print e.reason
        duration = ''
        #else:
      else:
        response.read()
        endTime = time()
        duration = (round(endTime-startTime, 3))
      if duration == '':
      # double check that the site is down and it was not just a temporary network issue
        startTime2 = time()
        try:
          response2 = urlopen(url)
        except Exception as e2:
          duration = ''
        else:
          response2.read()
          endTime = time()
          duration = (round(endTime-startTime2, 3))

      logMessage = "%s %s %s" % (curTime, app, duration)
      if (duration == '') or (duration > durationThreshold):
        domain = url.split("/")[2]
        if (duration == ''):
          subject = "%s on %s: Homepage load failed @ %s" % (app, domain, formattedTime)
          content = "Unable to access %s at %s" % (app, url)
          recipientList = outageMail
          recipient = ', '.join(outageMail)
          status = 'red'
          health = 'Inaccessible'
        else:
          subject = "%s on %s: Homepage load time %s seconds @ %s" % (app, domain, duration, formattedTime)
          content = "Performance degraded on %s at %s" % (app, url)
          recipientList = degradeMail
          recipient = ', '.join(degradeMail)
          status = 'orange'
          health = 'Degraded'
        if sendEmail == True:
          msg = MIMEMultipart('alternative')
          msg = MIMEText(content, 'html')
          msg['From'] = mailFrom
          msg['To'] = recipient
          msg.add_header('reply-to', replyTo)
          msg['Subject'] = subject
          # Send the message via our own SMTP server, but don't include the
          # envelope header.
          s = smtplib.SMTP(smtpHost)
          s.set_debuglevel(1)
          s.starttls()
          s.ehlo()
          s.sendmail(mailFrom, recipientList, msg.as_string())
          s.quit()
      else:
        status = 'green'
        health = 'Good'

      appDiv = (f"""
      <div class="app">
        <div class="appname">{app}:</div>
        <div class="appstatus"><img src='src/images/{status}light_small.png' title='Performance: {health}' alt='{status}'></div>
      </div>
      """).strip()
      statusRows += divider + appDiv
      divider = ("""<div class="divider"></div>""").strip()

      print (logMessage)

    line = urlFile.readline()


  #lastUpdate = systime.strftime('%-I:%M:%S %p %m/%d/%Y')
  lastUpdate = sysTime.strftime('%H:%M:%S %p %m/%d/%Y')
  htmlContent = (f"""
  <html>
  <head>
    <title>Web Application Status</title>
    <link href="src/css/siteMonitor.css" rel="stylesheet" type="text/css" />
  </head>
  <body>
    <div class="applist">
    {statusRows}
    </div>
    <div class="lastupdate">Last Updated: {lastUpdate}</div>
  </body>
  </html>
  """)

  webfile = open(statusPage,'w')
  webfile.write(htmlContent)
  webfile.close()

