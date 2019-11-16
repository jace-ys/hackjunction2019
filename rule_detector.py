import re
import json

# url-based tests
def ip_address(url):
    # return true if url has an ip address, otherwise false
    
    dec_pattern = '[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}'
    hex_pattern = '0x.{2}[.]' # not complete but if its gonna contain this pattern its anyway a hex IP address
    
    dec_match = re.search(dec_pattern, url)
    hex_match = re.search(hex_pattern, url)
    if dec_match:
        message = "An IP address is a sequence of numbers separated by three dots - here, it's %s. Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!" % dec_match.group(0)
        return message
    elif hex_match:
        message = "The URL of this site contains an IP address. An IP address is a sequence of numbers separated by three dots - here, it's %s. Now, this doesn't look like numbers at all! That's because theyre in a format called hexadecimal, which is easier for computers to read. Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!" % hex_match.group(0)
        return message
    return ""

url1 = 'http://125.98.3.123/fake.html'
url2 = 'http://0x58.0xCC.0xCA.0x62/2/paypal.ca/index.html'
#print(ip_address(url1))
#print(ip_address(url2))

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

def domain_dash(url):
    message = "This URL contains a '-'. Most websites do not contain this - if one does, it is likely a phishing website."
    if '-' in url:
        return True, message
    return False, ""

ccTLD_list = ['.ac', '.ad', '.ae', '.af', '.ai', '.al', '.am', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm'] # needs filling

def https_domain(url):
    message = "This URL contains 'https' in the domain of the URL. The domain is what comes after the 'www.' in the URL. While the start of the URL usually contains the pattern 'https', it should never appears in the domain part. If it does, it's most likely a phishing site!"
    parts = re.split('//', url)
    if len(parts) == 1:
        return 'https' in parts[0]
    elif 'http' in parts[0]:
        return any('https' in p for p in parts[1:])
    else:
        return any('https' in p for p in parts)
    
def perform_check(url):
    ip_result 
    
def prepare_message(data, url_ip, long_url, bank_check, info_check, grammar_check):
    # URL is the most important check so that goes first
    if data is None:
        data = {"isPhishing":True,
                "issues": []}
    if len(url_ip) > 0:
        data["issues"].append({'subject': "This URL contains an IP address.",
                               'textOne': url_ip})
    if long_url:
        data["issues"].append({'subject': "This URL is very long.",
                               'textOne': "Be wary of sites that have URLs this long, they're likely phishing sites.",
                               'textTwo': "Remember, checking the URL is one of the easiest ways to recognize a phishing site!"})
    if bank_check and not info_check:
        data["issues"].append({'subject': "This phishing site might be asking for your bank information.",
                                  'textOne': "You probably don't have a bank account yet, but you still shouldn't fill in any forms like this. Always ask your parents if it's ok to submit information to any website."})
    elif info_check and not bank_check:
        data["issues"].append({'subject': "It appears that this page is asking for personal information.",
                                  'textOne': "Phishing attackers try to trick you to give them your personal information, like your name or your address! When you are submitting any information to any website, ask your parents to check that it's ok."})
    elif info_check and bank_check:
        data["issues"].append({'subject': "You're on a phishing site that appears to be asking for your information.",
                                  'textOne': "Phishing attackers try to trick you to give them your personal information, like your name or your address! When you are submitting any information to any website, ask your parents to check that it's ok."})
    if grammar_check:
        data["issues"].append({'subject': "This page looks like it was written by a phisher!",
                                  'textOne': "Some phishing sites, like this one, are not written well. If you land on a webpage that contains weird language, go back - you're on a phishing site!",
                                  'textTwo': "Sometimes you might enter pages that are written in a foreign language. You're better off moving away from those as well - you can't know what's on the page."})
    if len(url_ip) == 0 and not long_url and not bank_check and not info_check and not grammar_check:
        data["issues"].append({'subject': "You're looking at a phishing site that is very hard to distinguish from a normal website.",
                               'textOne': "It's difficult to say what makes this a phishing site, as it looks very similar to a normal website. For some phishing sites, that is the case.",
                               'textTwo': "Besides inspecting the web page, you can also look at the address bar to distinguish phishing websites. Some phishing websites have weird URLs that differ from normal sites.",
                               'textThree': "Sometimes, even that doesn't work as the phishing attacker can be very deceptive. That's why you have assistants like me to protect you!"})
    with open('data.json', 'w') as f:
        json.dump(data, f)
    """elif redirection_double_slash_url():
        message = {'message': {'subject': "Hold up right there, that's a long URL!",
                               'textOne': "This URL actually consists of two URL separated by a '//'. This means that the site you're actually going to visit is the one that occurs after the '//'.",
                               'textTwo': "This is yet another method phishing attackers use to distract you!"}}
    elif bank_check and not info_check:
        message = {'message': {'subject': "You've landed on a phishing site that might be asking for your bank information!",
                                  'textOne': "You probably don't have a bank account yet, but you still shouldn't fill in any forms like this. Always ask your parents if it's ok to submit information to any website."}}
    elif info_check and not bank_check:
        message = {'message': {'subject': "It appears that this page is asking for personal information!",
                                  'textOne': "Phishing attackers try to trick you to give them your personal information, like your name or your address! When you are submitting any information to any website, ask your parents to check that it's ok."}
    elif info_check and bank_check:
        message = {'message': {'subject': "You're on a phishing site that appears to be asking for your information!",
                                  'textOne': "Phishing attackers try to trick you to give them your personal information, like your name or your address! When you are submitting any information to any website, ask your parents to check that it's ok."}
    elif grammar_check:
        message = {'message': {'subject': "Hmm, this page looks like it was written by a phisher!",
                                  'textOne': "Some phishing sites, like this one, are not written well. If you land on a webpage that contains weird language, go back - you're on a phishing site!",
                                  'textTwo': "Sometimes you might enter pages that are written in a foreign language. You're better off moving away from those as well - you can't know what's on the page!"}}
    else:
        message = {'message': 
        """
prepare_message(None, "", True, False, True, True)
