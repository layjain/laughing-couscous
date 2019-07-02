from flask import Flask, flash
from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
#import Laplace
import pandas
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import logreg
import os
from flask import session
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = 'static/uploaded'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def _clip(x, lower, upper):
    if lower>upper:
        raise ValueError('Cannot clip with lower more than upper')
    clipped=x
    if clipped<lower:
        return lower
    if clipped>upper:
        return upper
    return clipped
clip=np.vectorize(_clip)

def lap(mean, scale, size):
    #size=number of random nos needed
    rand=np.random.rand(size)-0.5
    randGen=mean-scale*np.sign(rand)*np.log(1-2*np.abs(rand))
    ###NOTE: contrary to given, np.sign returns 0 for 0, want to change?
    return randGen
    
def meanDP(x, lower, upper, epsilon):
    if upper<lower:
        raise ValueError
    n=len(x)
    sensitivity=(upper-lower)/n
    scale=sensitivity/epsilon
    x_clipped=clip(x, lower, upper)
    sensitiveValue=np.mean(x_clipped)
    DPrelease=sensitiveValue+lap(0, scale, 1)
    return {'release':DPrelease, 'true':sensitiveValue}

#Mean Release    
def generate_and_save_histogram (filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv",
                                 label='age',
                                 epsilon=1):
    #filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv"
    PUMSdata=pandas.read_csv(filepath)
    data=np.array(PUMSdata['age'])
    count=0
    release=[None for _ in range(2000)]
    true=[None for _ in range(2000)]
    print('Initialized empty lists')
    print('using epsilon', epsilon)
    for k in range(2000):
        DPmean=meanDP(x=data, lower=1, upper=125, epsilon=epsilon)
        release[k]=float(DPmean['release'])
        true[k]=DPmean['true']
        if release[k]<0:
            count+=1
    print('loop finished')
    plt.hist(release, bins=10)
##    plt.title("Histogram of released DP means")
##    plt.xlabel(" Differentially Private Mean Age")
##    plt.ylabel("frequency")
    print('Plot made')
    #plt.show()
    print(true[0])
    print(count)
    name='static/images/Laplace'+str(time.time())+'.png'
    plt.savefig(name)
    #plt.show()
    plt.close()
    print('fig saved')
    return name


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')
        
@app.route('/upload')
def upload():
    return render_template('upload.html', UPLOAD_STATUS='CLICK TO UPLOAD')

@app.route('/upload_process', methods=['GET','POST'])
def upload_process():
    session['filename']=None
    print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('upload.html', UPLOAD_STATUS='CLICK TO UPLOAD')
        file = request.files['file']
        if file.filename=='':
            flash('No selected file')
            filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv"
            df=pandas.read_csv(filepath)
            headers_list=list(df)
            OPTIONS_LIST=list_to_html(headers_list)
            print(OPTIONS_LIST)
            return render_template('upload.html', UPLOAD_STATUS='No File Selected', OPTIONS_LIST=OPTIONS_LIST)
        if file and allowed_file(file.filename):
            session['filename']=secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, session.get('filename')))
            df = pandas.read_csv(os.path.join(UPLOAD_FOLDER, session.get('filename')))
            headers_list=list(df)
            OPTIONS_LIST=list_to_html(headers_list)
            return render_template('upload.html', UPLOAD_STATUS='UPLOADED!', OPTIONS_LIST=OPTIONS_LIST)
        flash('only txt and csv allowed, Try Again!')
        return render_template('upload.html', UPLOAD_STATUS='WrongExtension, Try a csv or txt')


    
@app.route('/process', methods=['GET','POST'])
def process():
    print(request)
    print(dict(request.args))
    e = request.args.get('e','0.1')
    d = request.args.get('d', '0.1')
    try:
        epsilon=float(e)
    except:
        print('could not convert given epsilon to float')
        epsilon=0.1
    if session.get('filename')!=None:
        filepath = 'static/uploaded/'+session.get('filename')
        UPLOAD_STATUS='UPLOADED!'
        name=generate_and_save_histogram(filepath=filepath, epsilon=epsilon)
    else:
        UPLOAD_STATUS='USED DEFAULT FILE'
        name=generate_and_save_histogram(epsilon=epsilon)
    
    return render_template('upload.html', UPLOAD_STATUS=UPLOAD_STATUS, source=name)

@app.route('/dpml',methods=['GET','POST'])
def dpml_upload():
    return render_template('dpml.html', UPLOAD_STATUS='CLICK TO UPLOAD')


@app.route('/dpml_upload_php', methods=['GET','POST'])
def dpml_upload_process():
    print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('dpml.html', UPLOAD_STATUS='CLICK TO UPLOAD')
        file = request.files['file']
        if file.filename=='':
            flash('No selected file')
            return render_template('dpml.html', UPLOAD_STATUS='No File Selected')
        if file and allowed_file(file.filename):
            session['filename_dpml']=secure_filename(file.filename)
            print(session.get('filename_dpml'), 'as dpml filename')
            file.save(os.path.join(UPLOAD_FOLDER, session.get('filename_dpml')))
            
            return render_template('dpml.html', UPLOAD_STATUS='UPLOADED!')
        flash('only txt and csv allowed, Try Again!')
        return render_template('dpml.html', UPLOAD_STATUS='WrongExtension, Try a csv or txt')

@app.route('/dpml_process', methods=['GET', "POST"])
def dpml_process():
    print(request)
    print(dict(request.args))
    try:
        filename_dpml=session.get('filename_dpml')
    except:
        filename_dpml=None
    e = request.args.get('e','0.1')
    Lambda = request.args.get('lambda', '1')
    Degree=request.args.get('degree','6')
    epochs=request.args.get('epochs','800')
    alpha=request.args.get('alpha','1')
    
    epsilon=get_float(e, 0.1)
    Lambda=get_float(Lambda, 1)
    Degree=get_natural(Degree, 6, 'Could not convert given degree to int')
    epochs=get_natural(epochs, 800)
    alpha=get_float(alpha, 1.0)
    if filename_dpml != None:
        filepath = 'static/uploaded/'+filename_dpml
        UPLOAD_STATUS='UPLOADED!'
        filename_dpml=None
    else:
        filepath = "static/uploaded/logReg.txt"
        UPLOAD_STATUS='USED DEFAULT FILE'
        
    name=logreg.generate_and_save_graph(filepath=filepath, epsilon=epsilon, Lambda=Lambda,\
                                        degree=Degree, alpha=alpha, epochs=epochs)
    return render_template('dpml.html', source=name, UPLOAD_STATUS=UPLOAD_STATUS)

def get_float(var, default, failure_message=None):
    if failure_message==None:
        failure_message='could not convert'+str(var)+'to float'
    try:
        var=float(var)
    except:
        print(failure_message)
        var=default
    return var

def get_natural(var, default, failure_message=None):
    if failure_message==None:
        failure_message='could not convert'+str(var)+'to int'
    try:
        var=int(var)
    except:
        print(failure_message)
        var=default
    return var

def list_to_html(L):
    ans=''
    for i in range(1,len(L)+1):
        ans=ans+'<option value="'+str(i)+'">'+str(L[i-1])+'</option>'
    return ans
	
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
