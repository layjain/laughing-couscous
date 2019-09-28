$ = jQuery;
document.getElementById("SignUpButton").addEventListener("click", signup_js);

function signup_js() {
  var xhttp = new XMLHttpRequest();
  var username = document.getElementById("name").value;
  console.log("here it its-->");
  console.log(username);
  var password = document.getElementById("pass1").value;
  var remember = document.getElementById("checkpoint").value;
  var email = document.getElementById("email1").value;
  var params =
    "username=" +
    username +
    "&password=" +
    password +
    "&remember=" +
    remember +
    "&email=" +
    email;
  // xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  if (email === "") {
    document.getElementById("password_errors").innerHTML =
      "Email Cannot be Empty";
    return;
  }
  if (username === "") {
    document.getElementById("password_errors").innerHTML =
      "Username Cannot be Empty";
    return;
  }
  if (password === "") {
    document.getElementById("password_errors").innerHTML =
      "Password Cannot be Empty";
    return;
  }

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.open();
      document.write(this.responseText);
      document.close();
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
      console.log(this.responseText + "'");
      if (this.responseText != "") {
        $("#signup-username").tooltip("show");
      } else {
        $("#signup-username").tooltip("hide");
      }
    }
  };
  xhttp.open("GET", "/check_username_available?" + params, true);
  xhttp.send("username=" + username);
}

document
  .getElementById("signup-email")
  .addEventListener("focusout", check_email_available_js);
function check_email_available_js() {
  var xhttp = new XMLHttpRequest();
  var value = document.getElementById("signup-email").value;
  var params = "email=" + value;

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText + "'");
      if (this.responseText != "") {
        $("#signup-email").tooltip("show");
      } else {
        $("#signup-email").tooltip("hide");
      }
    }
  };
  xhttp.open("GET", "/check_email_available?" + params, true);
  xhttp.send();
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
