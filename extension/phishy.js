chrome.runtime.onMessage.addListener((message, sender) => {
  if (!sender.tab) {
    console.log(message);
    injectStyles();
    injectScripts();

    data.issues.forEach((issue, index) => {
      injectModal(index, issue);
    });
  }
});

const injectStyles = () => {
  let semanticStyle = document.createElement("link");
  semanticStyle.rel = "stylesheet";
  semanticStyle.href = chrome.runtime.getURL("assets/semantic.min.css");
  document.head.appendChild(semanticStyle);
};

const injectScripts = () => {
  let script = document.createElement("script");
  script.src = chrome.runtime.getURL("script.js");
  document.body.appendChild(script);

  let jQuery = document.createElement("script");
  jQuery.src = chrome.runtime.getURL("assets/jquery-3.4.1.slim.js");
  document.body.appendChild(jQuery);

  let semantic = document.createElement("script");
  semantic.src = chrome.runtime.getURL("assets/semantic.min.js");
  document.body.appendChild(semantic);
};

const injectModal = (index, issue) => {
  let div = document.createElement("div");
  div.insertAdjacentHTML("afterbegin", modal(index, issue));
  document.body.appendChild(div);
};

const modal = (index, issue) => {
  return `
<div class="ui basic modal" id="modal-${index}">
  <div class="image content">
    <img class="image" src=${chrome.runtime.getURL("assets/mascot.png")}>
    <div class="speech-bubble">
      <h4 class="subject">${issue.subject}</h4>
      <p class="text">${issue.text}</p>
      <small>- Phishy</small>
    </div>
  </div>
  <div class="actions">
    <div class="ui green ok inverted button">
      <i class="checkmark icon"></i>
      Got it!
    </div>
  </div>
</div>
`;
};

const data = {
  isPhishing: true,
  issues: [
    {
      subject: `The <span class="ui tooltip" data-tooltip="Address of website">URL</span> www.go00gle.com indicates a dodgy website`,
      text: "Most websites.."
    },
    {
      subject: "The page asks for your address",
      text: "Most websites.."
    },
    {
      subject: "The page uses dodge language",
      text: "Most websites.."
    }
  ]
};
