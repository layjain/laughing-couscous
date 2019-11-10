$ = jQuery;

$("#SignUpButton").click(function(e) {
  if (
    check_email_available_js() == "True" &&
    check_username_available_js() == "True"
  ) {
    console.log("checked");
    signup(e);
  }
});
function signup(e) {
  signup_form = $("#signup");
  username = $("#signup-username").val();
  password = $("#signup-password").val();
  email = $("#signup-email").val();
  signup_form.addClass("was-validated");
  console.log($("#signup .is-invalid")[0]);
  if (
    signup_form[0].checkValidity() === false ||
    $("#signup .is-invalid").length != 0
  ) {
    console.log("invalid");
    $("input[data-toggle=tooltip].is-invalid").tooltip("show");
    e.preventDefault();
    e.stopPropagation();
    return;
  }
  var xhttp = new XMLHttpRequest();
  var params =
    "username=" + username + "&password=" + password + "&email=" + email;
  e.preventDefault();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      $(".signup-feedback").show();
      if (this.responseText == "True") {
        $(".signup-feedback .signup-success").show();
        $(".signup-feedback .signup-error").hide();
      } else {
        $(".signup-feedback .signup-success").hide();
        $(".signup-feedback .signup-error").show();
      }
    }
  };
  xhttp.open("GET", "/register?" + params, true);
  xhttp.send();
}

document
  .getElementById("signup-username")
  .addEventListener("focusout", check_username_available_js);
function check_username_available_js() {
  var xhttp = new XMLHttpRequest();
  var username = document.getElementById("signup-username").value;
  var params = "username=" + username;

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText != "") {
        $("#signup-username").tooltip("show");
        $("#signup-username").addClass("is-invalid");
      } else {
        $("#signup-username").tooltip("hide");
        $("#signup-username").removeClass("is-invalid");
      }
    }
  };
  xhttp.open("GET", "/check_username_available?" + params, true);
  xhttp.send("username=" + username);
  return "True";
}

document
  .getElementById("signup-email")
  .addEventListener("focusout", check_email_available_js);
function check_email_available_js() {
  var xhttp = new XMLHttpRequest();
  var value = document.getElementById("signup-email").value;
  if (value == "") return;
  var params = "email=" + value;

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText != "") {
        $("#signup-email").tooltip("show");
        $("#signup-email")
          .addClass("is-invalid")
          .removeClass("is-valid");
      } else {
        $("#signup-email").tooltip("hide");
        $("#signup-email")
          .removeClass("is-invalid")
          .addClass("is-valid");
      }
    }
  };
  xhttp.open("GET", "/check_email_available?" + params, true);
  xhttp.send();
  return "True";
}

$("input[data-toggle='tooltip']").focus(function() {
  console.log("inside");
  $(this)
    .parents("form")
    .find("input[data-toggle=tooltip]")
    .each(function() {
      $(this).tooltip("hide");
    });
});
