let counter = 0;
const modalCount = document.querySelectorAll(".ui.basic.modal").length;

const show = () => {
  $(`#modal-${counter}`).modal("show");
  counter++;
  if (counter > modalCount) window.history.back();
};

document.onclick = event => {
  event.preventDefault();
  show();
};
