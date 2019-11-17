import re
import json
from parse import Parser
from phish_categorizer import PhishCategorizer, PhishCategory

# url-based tests
def ip_address(url):
    # return true if url has an ip address, otherwise false

    dec_pattern = '[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}'
    hex_pattern = '0x.{2}[.]0x.{2}[.]0x.{2}[.]0x.{2}'

    dec_match = re.search(dec_pattern, url)
    hex_match = re.search(hex_pattern, url)
    if dec_match:
        message = {'subject': "The <span class='ui tooltip' data-tooltip='web address'>URL</span> contains an <span class='ui tooltip' data-tooltip='a label for a device connected to a network.'>IP address</span>. Here, it's %s." % dec_match.group(0),
                               'text': "Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!"}
        return message
    elif hex_match:
        message = {'subject': "The <span class='ui tooltip' data-tooltip='web address'>URL</span> contains an <span class='ui tooltip' data-tooltip='a label for a device connected to a network.'>IP address</span>. Here, it's %s." % hex_match.group(0),
         'text': "Now, this doesn't look like numbers at all! That's because it's in a format called hexadecimal, which is easier for computers to read. Most websites' URLs do not contain IP addresses - if one does, it is likely a phishing website!"}
        return message
    return {}

url1 = 'http://125.98.3.123/fake.html'
url2 = 'http://0x58.0xCC.0xCA.0x62/2/paypal.ca/index.html'

def long_url(url):
    return len(url) > 54

def redirection_double_slash(url):
    message = "This URL actually consists of two URL separated by a '//'. This means that the site you're actually going to visit is the one that occurs after the '//'. This is one way phishing attackers can try to distract you!"
    splits = re.split('//', url)

    return len(splits) > 2 or len(splits[0]) > 7

def domain_dash(url):
    domain = get_domain(url)
    return '-' in domain

def at_url(url):
    return '@' in url

ccTLD_list = ['.ac', '.ad', '.ae', '.af', '.ai', '.al', '.am', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cu', '.cv', '.cw', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm'] # needs filling

def https_domain(url):
    message = "This URL contains 'https' in the domain of the URL. The domain is what comes after the 'www.' in the URL. While the start of the URL usually contains the pattern 'https', it should never appears in the domain part. If it does, it's most likely a phishing site!"
    domain = get_domain(url)
    return "https" in domain

def get_domain(url):
    if url.startswith('https://'):
        url = url[8:]
    elif url.startswith('http://'):
        url = url[7:]
    if url.startswith('www.'):
        url = url[4:]
    url= re.split('/', url)[0]
    return url


def get_issues(url):
    # checks on URL
    url_ip = ip_address(url)
    domain = get_domain(url)
    lengthy_url = long_url(url)
    redir = redirection_double_slash(url)
    dash = domain_dash(url)
    https = https_domain(url)
    at = at_url(url)

    # process html text
    p = Parser()
    url_text = p.scrape_text(url)

    # grammar, site category checks
    pc = PhishCategorizer(url_text)
    r = pc.categorize()
    res = pc.check_grammar()
    win = r == PhishCategory.set_win
    bank = r == PhishCategory.set_bank
    personal = r == PhishCategory.set_personal
    impersonate = r == PhishCategory.impersonate
    grammar = res > 20


    data = {"isPhishing":True,
            "issues": []}
    if len(url_ip) > 0:
        data["issues"].append(url_ip)
    if lengthy_url:
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='web address'>URL</span> is very long.",
                               'text': "Be wary of sites that have URLs this long, they're likely phishing sites."})
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='web address'>URL</span> is very long.",
                               'text': "Remember, checking the URL is one of the easiest ways to recognize a phishing site!"})
    if redir:
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='web address'>URL</span> actually consists of two URL separated by a '//'.",
                               'text': "This means that the site you're actually going to visit is the one that occurs after the '//'."})
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='web address'>URL</span> actually consists of two URL separated by a '//'.",
                               'text': "This is one way phishing attackers can try to distract you!"})
    if dash:
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='%s'>domain</span> contains a dash." % domain,
                               'text': "Most domains that contain a dash are from phishing websites."})
    if https:
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='%s'>domain</span> contains 'https'." % domain,
                               'text': "While the start of the <span class='ui tooltip' data-tooltip='web address'>URL</span> usually contains the pattern 'https', it should never appears in the domain part. If it does, it's most likely a phishing site!"})
    if at:
        data["issues"].append({'subject': "This <span class='ui tooltip' data-tooltip='web address'>URL</span> contains '@'.",
                               'text': "Anything that is written before the '@' is ignored by your web browser. Phishers use this character to distract you from the suspicious parts of the URL."})
    if bank:
        data["issues"].append({'subject': "This phishing site might be asking for your bank information.",
                                  'text': "You probably don't have a bank account yet, but you still shouldn't fill in any forms like this. Always ask your parents if it's ok to submit information to any website."})
        data["issues"].append({'subject': "This phishing site might be asking for your bank information.",
                                  'text': "If you were to submit your information to a site like this, the attackers could get access to your bank account and you could lose all your money!"})
    elif personal:
        data["issues"].append({'subject': "It appears that this page is asking for personal information.",
                                  'text': "Phishing attackers try to trick you to give them your personal information, like your name or your address! When you are submitting any information to any website, ask your parents to check that it's ok."})
        data["issues"].append({'subject': "It appears that this page is asking for personal information.",
                                  'text': "You should never tell strangers where you live. If you submitted information to a page like this, you could be doing just that!"})
    elif win:
        data["issues"].append({'subject': "This site looks like it's falsely promoting a reward to you.",
                                  'text': "Phishing attackers put up such 'free prizes' to try to attract your attention and have you submit information to claim your reward."})
        data["issues"].append({'subject': "This site looks like it's falsely promoting a reward to you.",
                                  'text': "It's not safe to give away your information online. Also, you won't actually be getting anything!"})
    elif impersonate:
        data["issues"].append({'subject': "This site looks like it's trying to impersonate a real company.",
                                  'text': "When logging in to any website that looks familiar, make sure that the URL is what you expect it to be and that the page does not contain any weird artifacts."})
    if grammar:
        data["issues"].append({'subject': "This page looks like it was written by a phisher!",
                                  'text': "Some phishing sites, like this one, are not written well. If you land on a webpage that contains weird language, go back - you're on a phishing site!"})
        data["issues"].append({'subject': "This page looks like it was written by a phisher!",
                                  'text': "Sometimes you might enter pages that are written in a foreign language. You're better off moving away from those as well - you can't know what's on the page."})
        data["issues"].append({'subject': "This page looks like it was written by a phisher!",
                                  'text': "Websites like this are usually for scams, where people try to take your money against fake products. You could be paying for something and not get anything! In addition, you might give someone your payment details and they could use them!"})
    if len(data["issues"]) == 0:
        data["issues"].append({'subject': "You're looking at a phishing site that is very hard to distinguish from a normal website.",
                               'text': "It's difficult to say what makes this a phishing site, as it looks very similar to a normal website. For some phishing sites, that is the case."})
        data["issues"].append({'subject': "You're looking at a phishing site that is very hard to distinguish from a normal website.",
                               'text': "Besides inspecting the web page, you can also look at the address bar to distinguish phishing websites. Some phishing websites have weird <span class='ui tooltip' data-tooltip='web address'>URLs</span> that differ from normal sites."})
        data["issues"].append({'subject': "You're looking at a phishing site that is very hard to distinguish from a normal website.",
                               'text': "Sometimes, even that doesn't work as the phishing attacker can be very deceptive. That's why you have assistants like me to protect you!"})

    data["issues"].append({'subject': "That's it for this website.",
                               'text': "You'll be redirected to where you were before. Try to remember what you've learned!"})

    return data
