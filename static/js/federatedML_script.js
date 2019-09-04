console.log('Hello from federatedML_script.js')

document.getElementById("JoinButton").addEventListener("click", Join_js);

function join_js(){
	var xhttp = new XMLHttpRequest();
	var ProjectID=document.getElementById("JoinID").value;
	console.log('ID input was-->')
	console.log(ProjectID)

	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      document.open();
	      document.write(this.responseText);
	      document.close();
	    }
	  };
	xhttp.open("GET", "/joinFederatedProject?ProjectID="+ProjectID, true);
	xhttp.send();
}
