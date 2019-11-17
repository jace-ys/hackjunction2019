# Phishy the Fish

<p align="center">
  <img width="300" alt="Phishy" src="https://github.com/jace-ys/hackjunction2019/blob/master/extension/assets/mascot.png">
</p>

## Problem

With smartphones and other digitally connected devices becoming ubiquitous amongst kids, there is a more pressing need than ever before to educate kids on how to protect themselves in the digital world - the curious and gullible nature of kids make them easy targets for falling prey to malicious cyber attacks such as phishing, cyber bullying and malware infection.

## Solution

We have developed Phishy the Fish in a bid to tackle the problem of phishing websites that might lead to unknowing kids leaking personal and private information on the web, or even installing malicious software. Phishy is a browser extension for Chrome targeted at kids, and aims not just to protect them from any malicious interactions with phishing websites, but most importantly, educate them about the consequences of visiting such sites, and how they can be easily identified. This will raise their awareness of such malicious web content, thus grooming them into digitally-literate netizens of the future.

### Software Architecture

<p align="center">
  <img width="800" alt="Architecture" src="https://github.com/jace-ys/hackjunction2019/blob/master/extension/assets/architecture.jpg">
</p>

### Implementation

Phishy comprises of 3 components.

1. Chrome extension:
   This was developed in JavaScript, HTML and CSS and functions as the "user interface" that kids interact with; it presents itself as our kid-friendly mascot, Phishy the Fish.
   If a visited is suspected to be phishing, Phishy blocks any interactions kids make with the website by overwriting the page's HTML DOM - clicks are overridden and do not do what they were intended to. Instead, clicks cause Phishy to popup on the screen and highlight the dubious content, explaining what's dubious about them and how they can be identified. Phishy also goes on to warn kids about the consequences of being phished, such as leaking their bank details, addresses and phone numbers, or installing malicious software. After that, Phishy redirects kids back to the previous site. To make Phishy more kid-friendly, we also provide tooltips for internet terminologies that they might not understand.

2. URL Analysing Backend:
   This service exposed via a Flask HTTP server takes a URL payload, and analyses the URL to determine if it's a potential phishing website before returning a boolean response value to the Chrome extension.
   The service categorise suspicious urls against checklist of conditions:

   - Compare the URL against a list of known “good/popular” sites
   - Check if the URL is an internationalized domain name (https://en.wikipedia.org/wiki/IDN_homograph_attack)
   - Check if the URL has many or too long subdomains (https://securityblog.switch.ch/2017/11/14/subdomain-hijacking/)
   - Check if the top-level domain of the URL matches the list of all valid top-level domains is maintained by the Internet Assigned Numbers Authority (IANA)(IANA) (https://www.icann.org/resources/pages/tlds-2012-02-25-en)

3. Content Analysing Backend: This service analyses the website's content and identifies the factors that make it classified as a phishing website. The text content is stripped from the website's HTML and the following is done:
   - Pre-processing using Natural Language Processing
   - Check if the website exceeds a certain threshold of grammatical errors
   - Uses a combination of sentiment analysis and keyword search to categorize the type of phishing attempt

# Future improvements

- Reduce latency for network round-trip or build some ML capabilities into extension
- For Phishy to be effective, it should be installed onto kids' devices and can only be disabled by their parents.
