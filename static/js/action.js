$ = jQuery;

$("#select-file").change(function(e) {
  file = e.target.files[0];
  size = file.size;
  unit = "Bytes";
  if (size > 1024) {
    size = Math.floor(size / 1024);
    unit = "KB";
  }
  $(".file-spec#file-name")
    .show()
    .text(file.name);

  $("figcaption .upload-caption").hide();
  $(".dataset-upload label")
    .css("white-space", "nowrap")
    .addClass("btn-outline")
    .text("Change File");
  $("#upload-data")
    .parent()
    .show();
  if (size >= 1024) {
    $("#upload-data").addClass("disabled");
    $(".size-error").show();
    $(".file-spec#file-size").hide();
  } else {
    $("#upload-data").removeClass("disabled");
    $(".size-error").hide();
    $(".file-spec#file-size")
      .show()
      .text("(" + size + " " + unit + ")");
  }
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
  $.ajax({
    type: "POST",
    url: "/upload_process",
    data: form_data,
    contentType: false,
    cache: false,
    processData: false,
    success: function(data) {
      $(".tab-select.fields").html($("<div/>").addClass("d-none tab-radios"));
      $.each(JSON.parse(data), function(key, item) {
        label = $("<label/>")
          .addClass("btn btn-outline")
          .attr("for", "field-" + item)
          .text(item);
        label.appendTo($(".tab-select.fields"));
        input = $("<input/>")
          .attr({
            type: "radio",
            name: "field",
            id: "field-" + item,
            value: item,
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
  $(this)
    .parents(".form")
    .find("*[data-hide]")
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

$("input[type='number'][min]").change(function() {
  value = parseFloat($(this).val());
  low = parseInt($(this).attr("min"));
  high = parseInt($(this).attr("max"));
  step = parseFloat($(this).attr("step"));
  if ($(this).attr("data-inclusive-min") == "False") low = low + step;
  if (value > high) $(this).val(high);
  if (value < low) $(this).val(low);
});

$("input[type=range]").each(function() {
  container = $("<div/>").addClass("col d-flex range-container");
  range = $(this);
  container.insertAfter(range);
  end = $("<div/>").addClass("range-extreme");
  min = range.attr("min");
  max = range.attr("max");
  if (range.attr("data-order-magnitude")) {
    max = max * 10 ** parseInt(range.attr("data-order-magnitude"));
    min = min * 10 ** parseInt(range.attr("data-order-magnitude"));
  }
  end
    .clone()
    .html(min)
    .appendTo(container);
  range.appendTo(container);
  end
    .clone()
    .html(max)
    .appendTo(container);
});
