let counter = 0;
const modalCount = document.querySelectorAll(".ui.basic.modal").length;

document.onclick = event => {
  event.preventDefault();
  $(`#modal-${counter}`)
    .modal({ duration: 1500, transition: "fade" })
    .modal("show");
  counter++;
  if (counter > modalCount) window.history.back();
};
