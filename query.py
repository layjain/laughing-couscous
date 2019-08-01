''''
functions needed for query.html to work
'''
def list_to_html_divs_tabs(l):
	ans=''
	for item in l:
		print(item)
		text_id=str(item)+"_text"
		ans+='<div id="'+str(item)+'"'+ ' class="tabcontent">'+'<h3>'+str(item)+'</h3>'\
		+'<form><textarea type="text" rows="3" cols="70" placeholder="Your text here" id="'+text_id+'"></textarea>'+'</form>'\
		+'<button id="'+str(item)+'_save_button" onclick="saveField('+"'"+ str(item) +"'" +')"> Save </button>'\
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

def save_item_text(item, item_text):
	file_name = 'attribute_'+item+'.txt'
	file_address = 'src/'+file_name
	f = open(file_address, 'w+')
	f.write(item_text)
	f.close()
	print('made and closed text file for ' +item)
	return