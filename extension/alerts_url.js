// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Retrieve relevant alerts for a site.
 */

goog.module('suspiciousSiteReporter.alerts');

const Tld = goog.require('publicsuffix.Tld');

/** @const {!Object<string, string>} Map of signals to messages for the UI. */
const ALERT_MESSAGES = {
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
};

/** @const {number} If a domain has this many subdomains or more, it is flagged. */
const NUM_SUSPICIOUS_SUBDOMAINS = 4;

/**
 * @const {number} If a domain has a subdomain with this many characters or
 * more, it is flagged.
 */
const SUSPICIOUS_SUBDOMAIN_LENGTH = 22;

/** {!Object<string, boolean>} Dictionary with top site domains as keys. */
let topSitesList = {};

/**
 * Returns the domain from a URL.
 * @param {string} url The URL of a page.
 * @return {string} The domain of the page.
 */
const getDomain = (url) => {
  return new URL(url).hostname;
};

/**
 * Returns the domain split into parts and excluding the tld.
 * @param {string} domain The domain of a page.
 * @return {!Array<string>} The domain of the page.
 */
const getDomainPartsWithoutTld = (domain) => {
  const suffix = '.' + Tld.getInstance().getTld(domain, /* icannOnly= */ false);
  return domain.slice(0, domain.lastIndexOf(suffix)).split('.');
};

/**
 * Determines whether the site uses an IDN.
 * @param {string} domain The domain of the page. Regardless of how the
 *     omnibox displays the URL, this should be encoded here.
 * @return {boolean} Whether domain has label starting with 'xn--' (is IDN).
 */
const isIDN = (domain) => {
  // Check that xn-- appears after '.' or at the start of the domain name.
  // Regex used instead of splitting by '.' because splitting causes
  // the international character encoding to get stripped out.
  const regexPunycode = /\.(xn--)/;
  return domain.startsWith('xn--') || regexPunycode.test(domain);
};

/**
 * Checks whether a site is in the top site list.
 * @param {string} domain The domain of the page.
 * @return {boolean} Whether the site is in the top 5k.
 */
const isTopSite = (domain) => {
  const suffix = '.' + Tld.getInstance().getTld(domain, /* icannOnly= */ false);
  const domainPartsWithoutTld = getDomainPartsWithoutTld(domain);
  const etldPlusOne =
      domainPartsWithoutTld[domainPartsWithoutTld.length - 1] + suffix;
  // The below assumes that the top sites list uses lower case only.
  return topSitesList[etldPlusOne.toLowerCase()];
};

/**
 * Fetches the top sites list from JSON.
 * @param {function(?)} callback Callback function.
 */
const fetchTopSites = (callback) => {
  const topSitesList = chrome.runtime.getURL('topsites.json');
  const xhr = new XMLHttpRequest();
  xhr.open('GET', topSitesList);
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      callback(JSON.parse(xhr.responseText));
    }
  };
  xhr.send();
};

/**
 * Sets the value of top sites list variable after fetching from JSON.
 */
const setTopSitesList = () => {
  fetchTopSites((topSites) => {
    topSitesList = topSites;
  });
};

/**
 * Determines whether user has visited specified domain within last 3 months.
 * We use 3 months because recently visited sites are more relevant and because
 * Chrome only stores 3 months of history. We also ignore sites visited today
 * for the first time to reduce false negatives.
 * @param {string} domain The domain of the page.
 * @return {!Promise<boolean>} Whether site was visited recently, before today.
 */
const visitedBeforeToday = (domain) => {
  // Visit time in Chrome history is in milliseconds since epoch, so convert
  // to this unit.
  const currentTime = new Date().getTime();
  const msInDay = 24 * 60 * 60 * 1000;
  const timeYesterday = currentTime - msInDay;
  const timeThreeMonthsAgo = currentTime - (msInDay * 90);
  return new Promise((resolve, reject) => {
    chrome.history.search(
        {
          text: '',  // empty string returns everything
          startTime: timeThreeMonthsAgo,
          endTime: timeYesterday,
          maxResults: 0  // unlimited
        },
        function(pages) {
          // If there is no browsing history returned, assume that the user has
          // browsing history turned off, meaning this signal is noisy. Resolve
          // true to effectively turn off this alert.
          if (pages.length === 0) resolve(true);
          resolve(pages.some((page) => getDomain(page.url) === domain));
        });
  });
};

/**
 * Determines whether the site has unusually many subdomains.
 * @param {string} domain The domain of the page.
 * @return {boolean} True if the site has many subdomains.
*/
const hasManySubdomains = (domain) => {
  const domainPartsWithoutTld = getDomainPartsWithoutTld(domain);
  return domainPartsWithoutTld.length >= NUM_SUSPICIOUS_SUBDOMAINS;
};

/**
 * Determines whether the site has unusually long subdomains.
 * @param {string} domain The domain of the page.
 * @return {boolean} True if the site has long subdomains.
 */
const hasLongSubdomains = (domain) => {
  const domainPartsWithoutTld = getDomainPartsWithoutTld(domain);
  return domainPartsWithoutTld.some(
      (subdomain) => subdomain.length >= SUSPICIOUS_SUBDOMAIN_LENGTH);
};

/**
 * Determines whether the site has multiple redirects through URL shorteners.
 * @param {!Set<string>} redirectUrls A list of unique URLs redirected through
 *     to land on the current site.
 * @return {boolean} Whether the redirect chain has multiple redirects
 *     through URL shorteners.
 */
const hasMultipleUrlShortenerRedirects = (redirectUrls) => {
  // List of some popular URL shorteners obtained from combining some public
  // lists. Limitation is that it is unable to cover custom branded links.
  const urlShorteners = new Set([
    'bc.vc',
    'bit.do',
    'bit.ly',
    'goo.gl',
    'is.gd',
    'ity.im',
    'lc.chat',
    'ow.ly',
    's2r.co',
    'soo.gd',
    'tinyurl.com',
    'tiny.cc',
  ]);
  let urlShortenerRedirects = 0;
  redirectUrls.forEach((url) => {
    if (urlShorteners.has(getDomain(url))) {
      // Only increase the redirect count if it was not an HTTPS upgrade.
      if (!(url.startsWith('https://') &&
            redirectUrls.has(url.replace('https', 'http')))) {
        urlShortenerRedirects += 1;
      }
    }
  });
  return urlShortenerRedirects > 1;
};

/**
 * Determines whether the site redirects through a suspicious TLD.
 * @param {!Set<string>} redirectUrls A list of unique URLs redirected through
 *     to land on the current site.
 * @return {boolean} Whether the redirect chain includes URLs with a suspicious
 *     TLD.
 */
const redirectsThroughSuspiciousTld = (redirectUrls) => {
  // List of TLDs that have a high percentage of spammy or malicious domain
  // registrations.
  const suspiciousTlds = new Set([
    '.accountant', '.bid',    '.click',  '.cricket', '.date',  '.download',
    '.faith',      '.gdn',    '.kim',    '.loan',    '.men',   '.party',
    '.pro',        '.racing', '.review', '.science', '.space', '.stream',
    '.top',        '.trade',  '.win',    '.work',    '.xyz',
  ]);
  for (const url of redirectUrls) {
    const tld =
        '.' + Tld.getInstance().getTld(getDomain(url), /* icannOnly= */ false);
    if (suspiciousTlds.has(tld)) return true;
  }
  return false;
};

/**
 * Determines if redirect chain initiated from outside program or webmail.
 * @param {!Array<!chrome.safeBrowsingPrivate.ReferrerChainEntry>} redirectChain
 *     The redirect chain starting from the latest user interaction.
 * @return {boolean} Whether the redirect chain was initiated from an outside
 *     program or webmail.
 */
const redirectsFromOutsideProgramOrWebmail = (redirectChain) => {
  if (redirectChain.length === 0) return false;
  // Initial domain list--should be updated on a rolling basis.
  const webmailDomains = [
    'connect.xfinity.com',
    'en.mail.qq.com',
    'e.mail.ru',
    'mail.aol.com',
    'mail.google.com',
    'mail.yahoo.com',
    'outlook.office365.com',
    'outlook.live.com',
    'service.mail.com',
  ];
  // The last entry in the redirect chain should be the original referrer.
  const initiatingEntry = redirectChain[redirectChain.length - 1];
  if (initiatingEntry && initiatingEntry.referrerUrl) {
    for (const webmailDomain of webmailDomains) {
      // Don't just do an exact match because some webmail domains might
      // include additional subdomains, e.g. mg.mail.yahoo.com.
      if (getDomain(initiatingEntry.referrerUrl).endsWith(webmailDomain)) {
        return true;
      }
    }
  }
  // When maybeLaunchedByExternalApp is true, this means that there's a
  // possibility the entry was launched by an external application, but it might
  // be a false positive. If false, the entry definitely was not launched
  // by an external application.
  if (initiatingEntry.maybeLaunchedByExternalApp) return true;
  return false;
};

/**
 * Returns the redirect URLs from a referrer chain.
 * @param {!Array<!chrome.safeBrowsingPrivate.ReferrerChainEntry>} redirectChain
 *     The redirect chain starting from the latest user interaction.
 * @return {!Set<string>} A list of URLs redirected through to land
 *     on the current site, including the final page URL.
 */
const getRedirectUrls = (redirectChain) => {
  const redirectUrls = new Set();
  for (const referrerEntry of redirectChain) {
    if (referrerEntry.referrerUrl) {
      redirectUrls.add(referrerEntry.referrerUrl);
    }
    if (referrerEntry.serverRedirectChain) {
      referrerEntry.serverRedirectChain.forEach((serverRedirect) => {
        redirectUrls.add(serverRedirect.url);
      });
    }
  }
  return redirectUrls;
};


/**
 * Filters referrer entries to those resulting from the latest user interaction.
 * @param {string} url The URL of the current tab.
 * @param {number} tabId The ID of the tab for which to fetch the referrer.
 * @return {!Promise<!Array<!chrome.safeBrowsingPrivate.ReferrerChainEntry>>}
 *     The redirect chain, which is a list of referrer entries starting from
 *     immediately after the latest user action.
 */
const fetchRedirectChain = (url, tabId) => {
  const referrerEntries = [];
  if (chrome.safeBrowsingPrivate &&
      chrome.safeBrowsingPrivate.getReferrerChain) {
    return new Promise((resolve, reject) => {
      chrome.safeBrowsingPrivate.getReferrerChain(tabId, (referrer) => {
        // Microsoft Edge returns null for the referrer chain.
        if (referrer) {
          for (const referrerEntry of referrer) {
            // The referrer chain is returned in order of recency, so after
            // seeing the first referrer chain entry that no longer contains a
            // client redirect, break out of the loop since subsequent entries
            // likely came from a user interaction, e.g. typing URL into the
            // URL bar or clicking a link, and were not part of the relevant
            // stream of redirects.
            if (referrerEntry.urlType !== 'CLIENT_REDIRECT') break;
            referrerEntries.push(referrerEntry);
          }
        }
        resolve(referrerEntries);
      });
    });
  }
  return Promise.resolve(referrerEntries);
};

/**
 * Compute alerts and populate alerts array.
 * @param {string} url The URL of the page.
 * @param {number} tabId The ID of the current tab.
 * @return {!Promise<!Array<string>>} List of alerts for page.
 */
const computeAlerts = async (url, tabId) => {
  const newAlerts = [];
  const domain = getDomain(url).toLowerCase();
  const visited = await visitedBeforeToday(domain);
  const redirectChain = await fetchRedirectChain(domain, tabId);
  const redirectUrls = getRedirectUrls(redirectChain);
  // Only warn about IDNs and redirect chain initiated from outside program when
  // the final URL is not on a top site.
  if (!isTopSite(domain)) {
    newAlerts.push(ALERT_MESSAGES['notTopSite']);
    if (isIDN(domain)) newAlerts.push(ALERT_MESSAGES['isIDN']);
    if (redirectChain && redirectsFromOutsideProgramOrWebmail(redirectChain))
      newAlerts.push(ALERT_MESSAGES['redirectsFromOutsideProgramOrWebmail']);
  }
  if (!visited) newAlerts.push(ALERT_MESSAGES['notVisitedBefore']);
  if (hasManySubdomains(domain))
    newAlerts.push(ALERT_MESSAGES['manySubdomains']);
  if (hasLongSubdomains(domain))
    newAlerts.push(ALERT_MESSAGES['longSubdomains']);
  if (hasMultipleUrlShortenerRedirects(redirectUrls))
    newAlerts.push(ALERT_MESSAGES['urlShortenerRedirects']);
  if (redirectsThroughSuspiciousTld(redirectUrls))
    newAlerts.push(ALERT_MESSAGES['redirectsThroughSuspiciousTld']);
  return Promise.resolve(newAlerts);
};

exports = {
  ALERT_MESSAGES,
  computeAlerts,
  fetchRedirectChain,
  getRedirectUrls,
  hasManySubdomains,
  hasMultipleUrlShortenerRedirects,
  hasLongSubdomains,
  isIDN,
  redirectsFromOutsideProgramOrWebmail,
  redirectsThroughSuspiciousTld,
  setTopSitesList,
  visitedBeforeToday,
};
