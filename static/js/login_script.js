// document.getElementById("LoginButton").addEventListener("click", login_js);
$("#login").submit(function(e) {
  e.preventDefault();
  console.log("executing login_js");
  var xhttp = new XMLHttpRequest();
  var username = document.getElementById("login-username").value;
  var password = document.getElementById("login-password").value;
  var remember = document.getElementById("login-remember").checked;
  var params =
    "username=" + username + "&remember=" + remember + "&password=" + password;

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText == false) {
        console.log(this.responseText);
        $("#login-password").tooltip("show");
      } else {
        document.open();
        document.write(this.responseText);
        document.close();
      }
    }
  };
  xhttp.open("POST", "/login_check?" + params, true);
  xhttp.send();
});
