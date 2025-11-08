import requests
import re
import time

site = raw_input('Enter a website: ')
try:
    tent = int(raw_input('OK, how many attempts do you want to make? '))
except:
    print 'Actions must be defined by Numbers # Correct #]'

print
print 'Loading...'
print

to_crawl = ['http://' + site]

crawled = set()
emails_found = set()

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.103 Safari/537.36'}

try:
    for i in range(tent):
        url = to_crawl[0]
        try:
            req = requests.get(url, headers=header)
        except:
            to_crawl.remove(url)
            crawled.add(url)
            continue

        html = req.text
        links = re.findall(r'<a href="?\'?(https?:\/\/[^"\'>]*)', html)
        #print 'Crawling:', url

        emails = re.findall(r'[\w\._-]+@[\w_-]+\.[\w\._-]+\w', html)
        #print emails

        to_crawl.remove(url)
        crawled.add(url)

        for link in links:
            if link not in crawled and link not in to_crawl:
                to_crawl.append(link)

        for email in emails:
            emails_found.add(email)
except Exception as error:
    print error
    print 'NOT FOUND'

if emails_found == set():
    print
    print "BAD, Try increasing the number of attempts."
else:
    print 'GOOD JOB !!!'
    time.sleep(1)
    print
    print 'Calculating Results...'
    time.sleep(3)
    print
for email in emails_found:
    print '### Found: ' + str(email)
print
print 'Number of Attempts = ' + str(tent)
