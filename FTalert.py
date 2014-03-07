#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re
import smtplib
import base64
import os, errno
import time
import sys

# constants
name = base64.b64decode("WWljaHVhbg==")
gmail_user = base64.b64decode("eWljaHVhbjIwMTA=")
gmail_pwd = base64.b64decode("anVzdGljZVdJTExiZVNFUlZFRA==")
FROM = base64.b64decode("eWljaHVhbjIwMTBAZ21haWwuY29t")
TO = ([base64.b64decode("eWljaHVhbjIwMTBAZ21haWwuY29t"), 
      base64.b64decode("Z2FjaGVuQGhvdG1haWwuY29t"),
      base64.b64decode("Y2h1bndlaUBnbWFpbC5jb20=")
      ]) #must be a list

# compile regex
member = re.compile('member')
reg = re.compile('class=\"thead\">')
number = re.compile('[0-9]')

try:
    while True:
        # grab and parse HTML
        url = "http://www.flyertalk.com/forum/mileage-run-deals-372/"
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        raw_data = soup.findAll("td",{"class":"thead"})

        # extract digits from objects
        i = 0
        digit = []
        for i in range(0, len(raw_data)):
            if member.findall(str(raw_data[i])):
                for s in str(raw_data[i]).split():
                    if reg.findall(s):
                        for n in s:
                            if number.findall(n):
                                digit.append(n)
                        break
                break

        # assemble the num of members
        k = len(digit)
        i = 0
        num_member = 0
        while k > 0:
            num_member += int(digit[k - 1]) * 10 ** i
            k = k - 1
            i = i + 1

        # output the number to a file
        try:
            with open("FTdatalog", 'ab') as f1:
                f1.write(str(num_member))
                f1.write('\n')
        except IOError:
            sys.exit(1)
        else:
            print "Success! Current visitors: " + str(num_member)
            f1.close()

        # read past num_member from file
        try:
            with open("FTdatalog", 'r') as f2:
                list = f2.read()
        except IOError:
            sys.exit(2)
        else:
            f2.close()

        if len(list.split()) > 1:
            previous_num = int(list.split()[-2])
        else:
            previous_num = float('Inf')

        def silentRemoveLog(filename):
            try:
                os.remove(filename)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

        # prevent overflown and preserve data continuity
        if len(list.split()) > 10000:
            silentRemoveLog("FTdatalog")
            try:
                with open("FTdatalog", 'ab') as f3:
                    f3.write(str(previous_num))
                    f3.write('\n')
                    f3.write(str(num_member))
                    f3.write('\n')
            except IOError:
                sys.exit(4)
            else:
                f3.close()

        percent = ((float(num_member) - float(previous_num)) / previous_num ) * 100

        def send_email():
            SUBJECT = "FT Mileage Run Forum User Surge Notice"
            TEXT = ("Hi there,\n\nThe Python script I wrote has detected " +
            "a surge of users on Flyertalk. Check " + url + " now!\n" + 
            "\nAs of last automated check, there were " + str(previous_num) + 
            " users online. Now, there are " + str(num_member) + " users online.\n" +
            "\nThis is an increase of " + str("%.2f" % (percent)) +
            "%.\n" + "\nBest,\n" + name)

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

        # send email if user increased by 50%
        if num_member >= previous_num * 1.5:
            send_email()
        time.sleep(1800)
except KeyboardInterrupt:
    print "Quitting the program."
except:
    print "Unexpected error: " + sys.exc_info()[0]
    raise




	