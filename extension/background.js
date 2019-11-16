chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    fetch("https://swapi.co/api/people/1/")
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (true) {
          messageContent({ isPhishing: true, ...data });
        }
      });
  }
});

const messageContent = payload => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    chrome.tabs.sendMessage(tabs[0].id, payload);
  });
};
