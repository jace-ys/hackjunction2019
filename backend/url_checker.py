import tldextract
import json
import datetime
from urllib.parse import urlparse
import asyncio
import re

ALERT_MESSAGES = {
    'isIDN': {
        "subject": "The domain is an <span class=\"ui icon\" data-tooltip=\"internationalized domain name\">IDN</span> or uses uncommon characters",
        "text": "The internationalized domain name (IDN) homograph attack is a way a malicious party may deceive computer users about what remote system they are communicating with, by exploiting the fact that many different characters look alike"
        },
    'longSubdomains': {
        "subject": "The URL has unusually long subdomains",
        "text": "Having control over a subdomain of a targeted domain name can be used to setup up a phishing website or other fake content. "
        },
    'notTopSite': {
<<<<<<< HEAD
        "subject": "This website is not visited frequently.",
=======
        "subject": "The website is not frequently visited",
>>>>>>> 03a717376fe67579ec2f34c84e7e327bf674e101
        "text": "Are you sure you've typed the url correctly?"
        },
    'manySubdomains': {
        "subject": "The URL has unusually many subdomains",
        "text": "Having control over a subdomain of a targeted domain name can be used to setup up a phishing website or other fake content. "

        },
    'noticann': {
        "subject": "The <span class=\"ui icon\" data-tooltip=\"top-level domain\">TLD</span> is not valid",
        "text": "Are you sure you've typed the url correctly?"
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
    return parsed.netloc

def getDomainPartsWithoutTld(domain):
    ext = tldextract.extract(domain)
    suffix=''
    if(ext.suffix ):
        suffix='.'+ext.suffix
    return  domain[:domain.rindex(suffix)].split('.')

def isIDN(domain):
    regexPunycode = "/\.(xn--)/"
    return domain.startswith('xn--') or re.search(regexPunycode, domain)

def isTopSite(domain):
    ext = tldextract.extract(domain)
    suffix=''
    if(ext.suffix):
        suffix='.'+ext.suffix
    domainPartsWithoutTld=getDomainPartsWithoutTld(domain)
    etldPlusOne = domainPartsWithoutTld[len(domainPartsWithoutTld) - 1] + suffix

    return etldPlusOne.lower() in topSitesList.keys()

def isiCann(domain):
    ext = tldextract.extract(domain)
    print(ext)
    suffix=''
    if(ext.suffix):
        suffix=ext.suffix
        print(ext.suffix)
    infile = open('icann.txt')
    count=0
    while True:
        line = infile.readline().replace('\n', '')

        if line.lower()==suffix:

            return True
        if not line:
            break
    return False

def hasManySubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return len(domainPartsWithoutTld) >= NUM_SUSPICIOUS_SUBDOMAINS

def hasLongSubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return any(len(subdomain) >= SUSPICIOUS_SUBDOMAIN_LENGTH for subdomain in domainPartsWithoutTld)

def computeAlerts(url):
    newAlerts = []
    domain = getDomain(url).lower()

    if not (isTopSite(domain)):
        newAlerts.append(ALERT_MESSAGES['notTopSite'])
        if (isIDN(domain)):
            newAlerts.append(ALERT_MESSAGES['isIDN'])
    if (hasManySubdomains(domain)):
        newAlerts.append(ALERT_MESSAGES['manySubdomains'])
    if (hasLongSubdomains(domain)):
        newAlerts.append(ALERT_MESSAGES['longSubdomains'])
    if not (isiCann(domain)):
        newAlerts.append(ALERT_MESSAGES['noticann'])
    return newAlerts

print(computeAlerts('http://www.phishtankcom.clichekdvd.pw'))
