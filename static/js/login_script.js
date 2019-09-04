document.getElementById("LoginButton").addEventListener("click", login_js);

function login_js(){
	console.log('executing login_js')
	var xhttp = new XMLHttpRequest();
	var username=document.getElementById("name").value;
	var password=document.getElementById("pass").value;
	var remember=document.getElementById("checkpoint").checked;
	console.log(remember)
	var params = "username="+username+"&remember="+remember+"&password="+password;

	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      document.open();
	      document.write(this.responseText);
	      document.close();
	    }
	  };
	xhttp.open("GET", "/login_check?"+params, true);
	xhttp.send();
}