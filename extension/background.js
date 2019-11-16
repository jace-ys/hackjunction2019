chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  const pageIsPhishing = isPhishing(tab.url);
  if (pageIsPhishing) {
    console.log("Phishing site");
    chrome.tabs.update(tabId, { url: "https://github.com" });
  }
});

const isPhishing = url => {
  console.log(url);
  return new RegExp(/google\.com/).test(url);
};

const messageContent = payload => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    chrome.tabs.sendMessage(tabs[0].id, payload);
  });
};

chrome.webNavigation;
