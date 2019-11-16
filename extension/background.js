chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    const pageIsPhishing = isPhishing(tab.url);
    if (pageIsPhishing) console.log("Phishing site");
    messageContent({ phishing: isPhishing(tab.url) });
  }
});

const isPhishing = url => {
  return true;
};

const messageContent = payload => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    chrome.tabs.sendMessage(tabs[0].id, payload);
  });
};
