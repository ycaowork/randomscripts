#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re
import smtplib
import time
import sys

# constants
name = "Your Name Here"
gmail_user = "Your gmail user name here"
gmail_pwd = "Your password here"
FROM = "Your email address here"
TO = (["Recipant's email address here"]) #must be a list

universities = (['University of ABC', 'U ABC',
                 'University of EFG', 'UEFG',
                 'U JKY', 'University of JKY'
                 ])
results = []

# regex
reject = re.compile('dRejected')
accept = re.compile('dAccepted')
degree = re.compile('Masters') # Ph.D

try:
    while True:
        print 'Running...gathering relevant results...'
        # grab and parse HTML
        url = "http://www.thegradcafe.com/survey/index.php?q=computer+science"
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        raw_data = soup.findAll("td")
        status_data = str(raw_data).split(',')

        i = 0
        k = 0
        j = 0
        for i in range(0, len(status_data)):
            for k in range(0, len(universities)):
                uni_name = re.compile(universities[k].lower())
                if uni_name.search(status_data[i].lower()) and degree.search(status_data[i + 2]):
                    results.append([universities[k], '', ''])
                    results[j][1] = status_data[i + 2][:-len('</td>')]
                    results[j][2] = "Unknown status. Please check online."
                    if reject.search(status_data[i + 3]):
                        results[j][2] = "Rejected"
                    if accept.search(status_data[i + 3]):
                        results[j][2] = "Accepted"
                    j = j + 1
                    break

        def printResultsToEmail():
            retVal = ''
            i = len(results) - 1
            while i >= 0:
                retVal += results[i][0] + ' ' + results[i][1] + ' ' + results[i][2]
                retVal += '\n'
                i = i - 1
            return retVal

        def send_email():
            SUBJECT = "GradCafe Forum Result Notice"
            TEXT = ("Hi there,\n\nThis program has compiled " +
            "a list of relevant grad school application results reported by users of GradCafe. " + 
            "You may check " + url + " now for more detail.\n" + 
            "\nSummary:\n\n" + printResultsToEmail() +
            "\n" + "\n--------------- End of Message ---------------\n")

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print "Successfully sent the mail."
            except:
                print "Failed to send mail."

        # send email if there is relevant info
        if len(results) > 5:
            send_email()
            results = []
        time.sleep(3600)
except KeyboardInterrupt:
    print "Quitting the program."
except:
    print "Unexpected error: " + sys.exc_info()[0]
    raise
