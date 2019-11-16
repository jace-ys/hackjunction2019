chrome.runtime.onMessage.addListener((message, sender) => {
  if (!sender.tab) {
    console.log(message);
    injectStyles();
    injectScripts();
    injectModal();

    overrideClicks();
  }
});

const overrideClicks = () => {
  let links = document.querySelectorAll("a");
  for (let link of links) {
    link.setAttribute("href", "javascript: show();");
  }

  let buttons = document.querySelectorAll("button");
  for (let button of buttons) {
    button.setAttribute("onclick", "javascript: show();");
  }

  let inputs = document.querySelectorAll("input[type='submit']");
  for (let input of inputs) {
    input.setAttribute("onclick", "javascript: show();");
  }
};

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

const injectModal = () => {
  let div = document.createElement("div");
  div.insertAdjacentHTML("afterbegin", modal());
  document.body.appendChild(div);
};

const modal = text => {
  return `
<div class="ui basic modal">
  <div class="image content">
    <img class="image" src=${chrome.runtime.getURL("assets/mascot.png")}>
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
