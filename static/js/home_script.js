console.log('Hello from home_script.js')

document.getElementById("SignUpButton").addEventListener("click", signup_js);

function signup_js(){
	var xhttp = new XMLHttpRequest();
	var username=document.getElementById("name").value;
	console.log('here it its-->')
	console.log(username)
	var password=document.getElementById("pass1").value;
	var remember = document.getElementById("checkpoint").value;
	var email = document.getElementById("email1").value;
	var params = "username="+username+"&password="+password+"&remember="+remember+"&email="+email;
	// xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	if (email === ''){
		document.getElementById('password_errors').innerHTML = 'Email Cannot be Empty'
		return
	}
	if (username === ''){
		document.getElementById('password_errors').innerHTML = 'Username Cannot be Empty'
		return
	}
	if (password === ''){
		document.getElementById('password_errors').innerHTML = 'Password Cannot be Empty'
		return
	}

	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      document.open();
	      document.write(this.responseText);
	      document.close();
	    }
	  };
	xhttp.open("GET", "/register?"+params, true);
	xhttp.send();
}

document.getElementById("email1").addEventListener("click", check_username_available_js);
function check_username_available_js(){
	var xhttp = new XMLHttpRequest();
	var username=document.getElementById("name").value;
	var password=document.getElementById("pass1").value;
	var email = document.getElementById("email1").value;
	var params = "username="+username+"&password="+password+"&email="+email;

	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      document.getElementById("UserNameAvailability").innerHTML = this.responseText;
	    }
	  };
	xhttp.open("GET", "/check_username_available?"+params, true);
	xhttp.send("username="+username+"&password="+password+"&email="+email);
}

