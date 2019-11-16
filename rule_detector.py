import re

# url-based tests
def ip_address(url):
    # return true if url has an ip address, otherwise false
    
    dec_pattern = '[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}'
    hex_pattern = '0x.{2}[.]' # not complete but if its gonna contain this pattern its anyway a hex IP address
    
    dec_match = re.search(dec_pattern, url)
    hex_match = re.search(hex_pattern, url)
    if dec_match:
        message = "This URL contains an IP address. An IP address is a sequence of numbers separated by three dots, in this URL, it's %s. Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!" % dec_match.group(0)
        return True, message
    elif hex_match:
        message = "This URL contains an IP address. An IP address is a sequence of numbers separated by three dots, in this URL, it's %s. Now, this might not look like numbers at all! That's because it's in a different format, called hexadecimal, which is easier for computers to read. Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!" % hex_match.group(0)
        return True, message
    return False, ""

url1 = 'http://125.98.3.123/fake.html'
url2 = 'http://0x58.0xCC.0xCA.0x62/2/paypal.ca/index.html'
print(ip_address(url1))
print(ip_address(url2))

def long_url(url):
    message = "This URL is very long! Be wary of sites that have URLs this long, they're likely phishing sites."
    if len(url) > 54:
        return True, message
    return False, ""

def redirection_double_slash(url):
    message = "This URL actually consists of two URL separated by a '//'. This means that the site you're actually going to visit is the one that occurs after the '//'. This is one way phishing attackers can try to distract you!"
    splits = re.split('//', url)
    if len(splits[0]) > 7:
        return True, message
    return False, ""

def dash(url):
    message = "This URL contains a '-'. Most websites do not contain this - if one does, it is likely a phishing website."
    if '-' in url:
        return True, message
    return False, ""

ccTLD_list = ['.ac', '.ad', '.ae', '.af', '.ai', '.al', '.am', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm'] # needs filling

def https_domain(url):
    message = "This URL contains 'https' in the domain part of the URL. The domain part is the middle part of the URL, for this website, it is While the start of the URL usually contains the pattern 'https', it never appears in the domain part "
    parts = re.split('//', url)
    if len(parts) == 1:
        return 'https' in parts[0]
    elif 'http' in parts[0]:
        return any('https' in p for p in parts[1:])
    else:
        return any('https' in p for p in parts)
    
