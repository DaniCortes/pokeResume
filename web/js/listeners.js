var registerForm = document.forms["register-form"];
registerForm.addEventListener("submit", function (event) {
  getpoke();
  event.preventDefault();
});

var $loading = $("#loading-div").hide();
$(document)
  .ajaxStart(function () {
    $loading.show();
  })
  .ajaxStop(function () {
    $loading.hide();
  });