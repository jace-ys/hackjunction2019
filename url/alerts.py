import tldextract
import json
import datetime
from urllib.parse import urlparse
import asyncio
import re
from promise import Promise

ALERT_MESSAGES = {
    'isIDN': 'Domain uses uncommon characters',
    'longSubdomains': 'Unusually long subdomains',
    'notTopSite': 'Site not in top 5k sites',
    'notVisitedBefore': 'Haven\'t visited site in the last 3 months',
    'manySubdomains': 'Unusually many subdomains',
    'redirectsThroughSuspiciousTld':
        'Site redirected through a TLD potentially associated with abuse',
    'redirectsFromOutsideProgramOrWebmail':
        'Visit maybe initiated from outside program or webmail',
    'urlShortenerRedirects': 'Has multiple redirects through URL shorteners',
  }

NUM_SUSPICIOUS_SUBDOMAINS = 4
SUSPICIOUS_SUBDOMAIN_LENGTH = 22
def setTopSitesList():
    with open('topsites.json') as json_file:
        return json.load(json_file)

topSitesList=setTopSitesList()

def getDomain(url):
    parsed=urlparse(url)
    return parsed.netloc

def getDomainPartsWithoutTld(domain):
    ext = tldextract.extract(domain)
    suffix = '.'+ext.suffix
    return domain[:domain.rindex(suffix)].split('.')

def isIDN(domain):
    regexPunycode = "/\.(xn--)/"
    return domain.startswith('xn--') or re.search(regexPunycode, domain)
 
def isTopSite(domain):
    ext = tldextract.extract(domain)
    suffix = '.'+ext.suffix
    domainPartsWithoutTld=getDomainPartsWithoutTld(domain)
    etldPlusOne = domainPartsWithoutTld[len(domainPartsWithoutTld) - 1] + suffix
    
    return etldPlusOne.lower() in topSitesList.keys()
        
    

# def visitedBeforeToday(domain):
#     currentTime = datetime.datetime.now()
#     timeYesterday = datetime.timedelta(days=-1)
#     DD = datetime.timedelta(days=-90)
#     timeThreeMonthsAgo = currentTime - DD

def hasManySubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return len(domainPartsWithoutTld) >= NUM_SUSPICIOUS_SUBDOMAINS

def hasLongSubdomains(domain):
    domainPartsWithoutTld = getDomainPartsWithoutTld(domain)
    return any(len(subdomain) >= SUSPICIOUS_SUBDOMAIN_LENGTH for subdomain in domainPartsWithoutTld)

def redirectsThroughSuspiciousTld(redirectUrls):
    suspiciousTlds = [
      '.accountant', '.bid',    '.click',  '.cricket', '.date',  '.download',
      '.faith',      '.gdn',    '.kim',    '.loan',    '.men',   '.party',
      '.pro',        '.racing', '.review', '.science', '.space', '.stream',
      '.top',        '.trade',  '.win',    '.work',    '.xyz',
    ]
    for url in redirectUrls:
        ext = tldextract.extract(domain)
        suffix = '.'+ext.suffix
        if any(tld in s for s in suspiciousTlds):
            return True
    return False

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

    return newAlerts

print(computeAlerts('https://www.secure.runescape.com-v.cz/'))