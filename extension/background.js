chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    fetch(`http://localhost:5000/check-phishing?url=${tab.url}`)
      .then(response => response.json())
      .then(data => {
        if (data.isPhishing) {
          messageContent(data);
        }
      });
  }
});

const messageContent = payload => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    if (tabs.length > 0) {
      chrome.tabs.sendMessage(tabs[0].id, payload);
    }
  });
};
