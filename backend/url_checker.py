import tldextract
import json
import datetime
from urllib.parse import urlparse
import asyncio
import re
from promise import Promise

ALERT_MESSAGES = {
    'isIDN': {
        "subject": "The domain is an <span class=\"ui icon\" data-tooltip=\"internationalized domain name\">IDN</span> or uses uncommon characters",
        "textOne": "The internationalized domain name (IDN) homograph attack is a way a malicious party may deceive computer users about what remote system they are communicating with, by exploiting the fact that many different characters look alike"
        },
    'longSubdomains': {
        "subject": "The URL has unusually long subdomains",
        "textOne": "Having control over a subdomain of a targeted domain name can be used to setup up a phishing website or other fake content. "
        },
    'notTopSite': {
        "subject": "The site is not in top 5k sites",
        "textOne": "Are you sure you've typed the url correctly?"
        },
    'manySubdomains': {
        "subject": "The URL has unusually many subdomains",
        "textOne": "Having control over a subdomain of a targeted domain name can be used to setup up a phishing website or other fake content. "
            
        },
    'noticann': {
        "subject": "The <span class=\"ui icon\" data-tooltip=\"top-level domain\">TLD</span> is not valid",
        "textOne": "Are you sure you've typed the url correctly?"
        }
  }

NUM_SUSPICIOUS_SUBDOMAINS = 4
SUSPICIOUS_SUBDOMAIN_LENGTH = 19
def setTopSitesList():
    with open('topsites.json') as json_file:
        return json.load(json_file)

topSitesList=setTopSitesList()

def getDomain(url):
    parsed=urlparse(url)
    print(parsed)
    return parsed.netloc

def getDomainPartsWithoutTld(domain):
    ext = tldextract.extract(domain)
    suffix=''
    if(ext.suffix ):
        suffix='.'+ext.suffix
        print(suffix)
    print(domain[:domain.rindex(suffix)].split('.'))
    return  domain[:domain.rindex(suffix)].split('.')

def isIDN(domain):
    regexPunycode = "/\.(xn--)/"
    return domain.startswith('xn--') or re.search(regexPunycode, domain)
 
def isTopSite(domain):
    ext = tldextract.extract(domain)
    suffix=''
    if(ext.suffix):
        suffix='.'+ext.suffix
        print(suffix)
    domainPartsWithoutTld=getDomainPartsWithoutTld(domain)
    etldPlusOne = domainPartsWithoutTld[len(domainPartsWithoutTld) - 1] + suffix
    
    return etldPlusOne.lower() in topSitesList.keys()
           
def isiCann(domain):
    ext = tldextract.extract(domain)
    suffix=''
    if(ext.suffix):
        suffix=ext.suffix
        print(suffix)
    infile = open('icann.txt', 'r')
    count=0
    while True:
        line = infile.readline()
        if not line: break
        return suffix.find(line.lower())!=-1
            
def hasManySubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return len(domainPartsWithoutTld) >= NUM_SUSPICIOUS_SUBDOMAINS

def hasLongSubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return any(len(subdomain) >= SUSPICIOUS_SUBDOMAIN_LENGTH for subdomain in domainPartsWithoutTld)

# def redirectsThroughSuspiciousTld(redirectUrls):
#     suspiciousTlds = [
#       '.accountant', '.bid',    '.click',  '.cricket', '.date',  '.download',
#       '.faith',      '.gdn',    '.kim',    '.loan',    '.men',   '.party',
#       '.pro',        '.racing', '.review', '.science', '.space', '.stream',
#       '.top',        '.trade',  '.win',    '.work',    '.xyz',
#     ]
#     for url in redirectUrls:
#         ext = tldextract.extract(domain)
#         suffix = '.'+ext.suffix
#         if any(tld in s for s in suspiciousTlds):
#             return True
#     return False

def computeAlerts(url):
    newAlerts = []
    domain = getDomain(url).lower() 

    if not(isTopSite(domain)):
        newAlerts.append(ALERT_MESSAGES['notTopSite'])
        if(isIDN(domain)):
            newAlerts.append(ALERT_MESSAGES['isIDN'])
    
    if (hasManySubdomains(domain)):
        newAlerts.append(ALERT_MESSAGES['manySubdomains'])
    if (hasLongSubdomains(domain)):
        newAlerts.append(ALERT_MESSAGES['longSubdomains'])
    if not (isiCann(domain)):
        newAlerts.append(ALERT_MESSAGES['noticann'])
    return newAlerts

print(computeAlerts('http://www.phishtankcom.clichekdvd.pw'))