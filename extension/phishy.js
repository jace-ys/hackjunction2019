chrome.runtime.onMessage.addListener((message, sender) => {
  if (!sender.tab) {
    console.log(message);
    replaceAllLinks();
    replaceWord(/the/g, "no");
  }
});

const replaceAllLinks = () => {
  let links = document.getElementsByTagName("a");
  for (let link of links) {
    link.onclick = function() {
      alert("Hello");
      return false;
    };
  }
};

const replaceWord = (word, newWord) => {
  document.body.innerHTML = document.body.innerHTML.replace(word, newWord);
};
