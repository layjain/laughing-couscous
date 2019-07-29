console.log("Im here")

document.getElementById("Query-Button").addEventListener("click", query_js);

function query_js(){
	var xhttp = new XMLHttpRequest();
		var e=document.getElementById("epsilon").value;
		var low=document.getElementById("min").value;
		var high=document.getElementById("max").value;
		var qiid = document.getElementById("qiid").value;
		var dpid = document.getElementById("dpid").value;

		xhttp.onreadystatechange = function() {
		    if (this.readyState == 4 && this.status == 200) {
		      document.open();
		      document.write(this.responseText);
		      document.close();
		    }
		  };
		xhttp.open("GET", "/query_process?e="+e+"&high="+high+"&low="+low+"&dpid="+dpid+"&qiid="+qiid, true);
		xhttp.send();
}