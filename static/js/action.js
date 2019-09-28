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
    .css("white-space", "nowrap")
    .addClass("btn-outline")
    .text("Change File");
  $("#upload-data")
    .parent()
    .show();
});
// trigger only when file is uploaded first time

$("#upload-data").click(function() {
  $(".dataset-upload label").css("white-space", "unset");
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
  var form_data = new FormData();
  form_data.append("file", $("#select-file")[0].files[0]);
  console.log(form_data);
  $.ajax({
    type: "POST",
    url: "/upload_process",
    data: form_data,
    contentType: false,
    cache: false,
    processData: false,
    success: function(data) {
      $.each(JSON.parse(data), function(key, item) {
        label = $("<label/>")
          .addClass("btn btn-outline")
          .attr("for", "field-" + item.toLowerCase())
          .text(item);
        label.appendTo($(".tab-select.fields"));
        input = $("<input/>")
          .attr({
            type: "radio",
            name: "field",
            id: "field-" + item.toLowerCase(),
            value: item.toLowerCase(),
            required: "required"
          })
          .addClass("tab-radio");
        input.appendTo($(".tab-select.fields .tab-radios"));
      });
      $("#field-type").show();
    }
  });
});

$(".tab-radios").on("change", ".tab-radio", function() {
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
  target = $(this).attr("data-control");
  $(".control-hidden")
    .removeClass("control-hidden")
    .show();
  $(".control-hidden")
    .find("input")
    .prop("required", true);
  // });
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
      $(this)
        .addClass("control-hidden")
        .hide();
      $(this)
        .find("input")
        .prop("required", false);
    }
  });
});

$("form.needs-validation").submit(function(e) {
  if (this.checkValidity() === false) {
    e.preventDefault();
    e.stopPropagation();
  }
  $(this).addClass("was-validated");
});

// INPUT SLIDER TO TEXT
$("input[type='range']").on("input", function() {
  id = $(this)
    .attr("id")
    .replace("-range", "");
  $("#" + id).val($(this).val());
});
$(".range-value").on("input", function() {
  id = $(this).attr("id") + "-range";
  $("#" + id).val($(this).val());
});
