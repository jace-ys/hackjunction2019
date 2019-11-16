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
   This was developed in JavaScript, HTML and CSS and functions as the "user interface" that kids interact with; it presents itself as our kid-friendly mascot, Phishy the Fish. Whenever a kid visits a website, the extension sends a request to our backend which returns a response of whether the site is a potential phishing website as well as information about any dubious content on the page.
   If the site is deemed to be phishing, Phishy blocks any interactions kids make with the website - clicks are overridden and do not do what they were intended to. Instead, clicks cause Phishy to popup on the screen and highlight the dubious content, explaining what's dubious about them and how they can be identified. Phishy also goes on to warn kids about the consequences of being phished, such as leaking their bank details, addresses and phone numbers, or installing malicious software. After that, Phishy redirects kids back to the previous site. To make Phishy more kid-friendly, we also provide tooltips for internet terminologies that they might not understand.

2. URL Analysing Backend

3. Content Analysing Backend

# Future improvements

For Phishy to be effective, it should be installed onto kids' devices and can only be disabled by their parents.
