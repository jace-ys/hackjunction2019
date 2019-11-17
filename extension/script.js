let counter = 0;
const modalCount = document.querySelectorAll(".ui.basic.modal").length;
let synth = window.speechSynthesis;

document.onclick = event => {
  event.preventDefault();
  $(`#modal-${counter}`)
    .modal({ duration: 1500, transition: "fade" })
    .modal("show");

  let subject = $(`#modal-${counter} .subject`).text();
  let utterSubject = new SpeechSynthesisUtterance(subject);
  speak(utterSubject);

  let text = $(`#modal-${counter} .text`).text();
  let utterText = new SpeechSynthesisUtterance(text);
  speak(utterText);

  counter++;
  if (counter > modalCount) window.history.back();
};

const speak = async text => {
  let voices = await synth.getVoices();
  text.voice = voices[48];
  synth.speak(text);
};
