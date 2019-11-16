chrome.runtime.onMessage.addListener((message, sender) => {
  if (!sender.tab) {
    console.log(message);
    // Code for modify link click
    // removeAllLinks();
    // let script = "'alert(123);'"
    // replaceWord(/<a /g, "<a onClick=" + script);
    // replaceWord(/<a>/g, "<a onClick=" + script + ">");

    createElement();

    // Code for make all link to pop up window
    //   removeAllLinks();
    //   let popupURL = "http://google.com";
    //   let script =
    //     "'window.open(\"" + popupURL + '","name","height=200,width=150");\'';
    //   replaceWord(/<a /g, "<a onClick=" + script);
    //   replaceWord(/<a>/g, "<a onClick=" + script + ">");
  }
});

const removeAllLinks = () => {
  let links = document.getElementsByTagName("a");
  for (let link of links) {
    link.removeAttribute("href");
  }
  console.log("All removed");
};

const replaceWord = (word, newWord) => {
  document.body.innerHTML = document.body.innerHTML.replace(word, newWord);
};

const createElement = () => {
  let btn = document.createElement("BUTTON");
  btn.innerHTML = "CLICK ME";
  btn.onabort = "https://github.com";
  document.body.appendChild(btn);
};
