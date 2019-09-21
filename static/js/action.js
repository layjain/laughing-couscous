$ = jQuery;

$("#select-file").change(function(e) {
  console.log(e.target.files[0]);
  file = e.target.files[0];
  $(".file-spec#file-name")
    .show()
    .text(file.name);
  $(".file-spec#file-size")
    .show()
    .text("(" + file.size + " bytes)");

  $("figcaption .upload-caption").hide();
  $(".dataset-upload label")
    .addClass("btn-outline")
    .text("Change File");
  $(".upload-btns>div:last-child").show();
});
// trigger only when file is uploaded first time

$("#upload-data").click(function() {
  $(this)
    .parents(".upload-form")
    .addClass("dataset-selected col-5")
    .removeClass("col-12");
  $(this)
    .parents(".upload-form")
    .parent()
    .find(".data-graph")
    .show();
  $(this)
    .parent()
    .hide();
});

$(".tab-radio").change(function() {
  $(this)
    .parents(".tab-select")
    .find("label.btn")
    .each(function() {
      $(this).removeClass("selected");
    });
  type = $(this).attr("name");
  value = $(this).val();

  $("." + type + "s label.btn[for='" + type + "-" + value + "']").addClass(
    "selected"
  );
});

$("label[data-control]").click(function() {
  console.log("clicked");
  target = $(this).attr("data-control");
  $(".control-hidden").each(function() {
    child = $(this)
      .find("*[data-hide]")
      .insertAfter($(this));
    $(this).remove();
  });
  $("*[data-hide]").each(function() {
    source = $(this).attr("data-hide");
    if (source.indexOf(target) >= 0) {
      $(this).removeClass("selected");
      $(this).attr("for")
        ? $("#" + $(this).attr("for"))
            .prop("selected", false)
            .prop("checked", false)
        : "";
      console.log($("#" + $(this).attr("for")).val());
      container = $("<div/>")
        .addClass("control-hidden")
        .insertAfter($(this))
        .hide();
      $(this).appendTo(container);
    }
  });
});

(function() {
  "use strict";
  window.addEventListener(
    "load",
    function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName("needs-validation");
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener(
          "submit",
          function(event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });
    },
    false
  );
})();
