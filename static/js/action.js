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
  if (size >= 1024 * 5) {
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
      // data = JSON.parse(data);
      $(".tab-select.fields").each(function() {
        radios = $("<div/>").addClass("d-none tab-radios");
        $(this).html(radios);
        input_type = $(this).attr("data-childType");
        type = $(this).attr("data-type");
        data_attr = null;
        require = input_type == "radio" ? true : false;
        $.each(JSON.parse(data["__" + type + "_options__"]), (key, item) => {
          label = $("<label/>")
            .addClass("btn btn-outline")
            .attr("for", "field-" + type + "-" + item.trim())
            .text(item.trim());
          if ($(this).attr("data-linked")) {
            label.attr({
              "data-title":
                item.trim() +
                " is already selected as " +
                $(this)
                  .attr("data-linked")
                  .toUpperCase() +
                ". Please unselect that to select this as " +
                type.toUpperCase(),
              "data-toggle": "tooltip",
              "data-trigger": "manual",
              "data-placement": "top"
            });
          }
          label.appendTo($(this));
          input = $("<input/>")
            .attr({
              type: input_type,
              name: "field-" + type,
              id: "field-" + type + "-" + item.trim(),
              value: item.trim()
            })
            .prop({ required: require })
            .addClass("tab-radio");
          input.appendTo(radios);
        });
        window.min_max = data;
        template = $("#bound-template").clone();
        $(".bounds-table tbody").html(template);
      });
      $("#field-type").show();
    }
  });
});

$(".tab-select").on("change", ".tab-radio", function() {
  var node = $(this).attr("type");
  var tab_select = $(this).parents(".tab-select");
  if (node === "radio") {
    tab_select.find("label.btn").each(function() {
      $(this).removeClass("selected");
    });
  }
  var type = $(this).attr("name");
  var value = $(this).val();
  $("label.btn[for='" + type + "-" + value + "']").toggleClass("selected");
  if (tab_select.attr("data-linked")) {
    var linked_type = type.replace(
      "-" + tab_select.attr("data-type"),
      "-" + tab_select.attr("data-linked")
    );
    if ($("input[id='" + linked_type + "-" + value + "']")) {
      $("label.btn[for='" + linked_type + "-" + value + "']").addClass(
        "disabled"
      );
      $("input[id='" + linked_type + "-" + value + "']").prop("disabled", true);
      disabled_check();
    }
  }
  if (tab_select.is("[data-bounds]") && tab_select.attr("data-type") == "x") {
    if (!$("*[id='bound-" + value + "']").length) {
      var row = $("#bound-template").clone();
      row.attr({ id: "bound-" + value, "data-feature-type": type }).show();
      row.find(".bound-feature").text(value);
      var step = (window.min_max[value][1] - window.min_max[value][0]) / 200;
      row.find("#lower-bound").attr({
        id: "lower-bound-" + value,
        value: window.min_max[value][0],
        step: step
      });
      row.find("#upper-bound").attr({
        id: "upper-bound-" + value,
        value: window.min_max[value][1],
        step: step
      });
      row.appendTo($(".bounds-table tbody"));
      $("#bounds").show();
      console.log(window.min_max);
    }
    // Check rows
    var rows = $(".bounds-table tbody tr").slice(1);
    rows.each(function() {
      var val = $(this)
        .attr("id")
        .replace("bound-", "");
      var type = $(this).attr("data-feature-type");
      if (!$("*[id='" + type + "-" + val + "']").prop("checked"))
        $(this).remove();
    });
    if ($(".bounds-table tbody tr").length <= 1) {
      $("#bounds").hide();
    }
  }
});

disabled_check = function() {
  $(".tab-select label.btn.disabled").each(function() {
    var select = $(this).parents(".tab-select");
    console.log($("input[id='" + $(this).attr("for") + "']"));
    var radio = $("input[id='" + $(this).attr("for") + "']");
    var type = $(radio).attr("name");
    var linked_type = type.replace(
      "-" + select.attr("data-type"),
      "-" + select.attr("data-linked")
    );
    var value = $(radio).val();
    if (!$("*[id='" + linked_type + "-" + value + "']").prop("checked")) {
      $(radio).prop("disabled", false);
      $("label.btn[for='" + type + "-" + value + "']").removeClass("disabled");
    }
  });
};

check_bounds_row = function() {};

$(".tab-select").on("mouseenter", "label.btn.disabled", function() {
  $(this).tooltip("show");
});
$(".tab-select").on("mouseleave", "label.btn.disabled", function() {
  $(this).tooltip("hide");
});

$("label[data-control]").click(function() {
  target = $(this).attr("data-control");
  container = $(this).parents(".form");
  container
    .find(".control-hidden")
    .find("input")
    .each(function() {
      $(this).prop("required", true);
    });
  container
    .find("*[data-hide]")
    .removeClass("control-hidden")
    .show();
  container.find("*[data-hide]").each(function() {
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
        .each(function() {
          $(this).prop("required", false);
        });
      $(this)
        .find("label.selected")
        .each(function() {
          $(this).removeClass("selected");
          src = $(this).attr("for");
          $("#" + src).prop("checked", false);
        });
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
  if ($(this).attr("data-inclusive-min") == "False" && value === low) {
    $(this).tooltip("show");
    $(this).addClass("data-invalid");
    return;
  }
  $(this).removeClass("data-invalid");
  if (value > high) $(this).val(high);
  if (value < low) $(this).val(low);
});

$("input[data-toggle='tooltip']").focus(function() {
  $(this).tooltip("hide");
  console.log("in");
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
