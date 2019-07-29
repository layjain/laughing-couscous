''''
functions needed for query.html to work
'''
def list_to_html_divs_tabs(l):
	ans=''
	for item in l:
		text_id=str(item)+"_text"
		ans+='<div id="'+str(item)+'"'+ ' class="tabcontent">'+'<h3>'+str(item)+'</h3>'\
		+'<form><textarea type="text" rows="3" cols="70" placeholder="Your text here" id="'+text_id+'"></textarea>'+'</form>'\
		+'</div>'
	return ans

def list_to_html_tabs(l):
	ans=''
	for item in l:
		item=str(item)
		ans+='<button class="tablinks" onclick="openField(event, '+"'"+item+"'"+')">'+item+'</button>'
	return ans

def show_download_part(name):
	return '''
	<div id="download part">
	Your Differentially Private document is ready! Click here to
	<a href="/static/css/{}" download='DiffPriv_PRIVAZ.txt'>
		Download
	</a>
	</div>
	'''.format(name)