from flask import Flask, flash
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
#import Laplace
import pandas
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import logreg
import query as query_src
import os
basedir=os.path.abspath(os.path.dirname(__file__))
from flask import session
import tqdm
import src
import subprocess
import shutil
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login import UserMixin, login_required

ALLOWED_EXTENSIONS = set(['txt', 'csv'])
UPLOAD_FOLDER = 'static/uploaded'

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_txt(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ['txt']

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

def bootstrap(x,n, y=None):
    index=np.random.choice(range(1, len(x)+1, 1), size=n, replace=True)
    if y==None:
        return [x[i] for i in index]
    else:
        return [[x[i] for i in index], [y[i] for i in index]]
    
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

def medianRelease(x, lower, upper, epsilon, nbins=0):
    #x is a np vector
    n=len(x)
    if nbins==0:
        bins=np.array(range(int(np.floor(lower)), int(np.ceil(upper)+1)), dtype='float32')
        nbins=len(bins)
    else:
        ######## CHECK THIS PART OF CODE ############
        bins=np.linspace(lower, upper, num=int(nbins))

    x_clipped=clip(x, lower, upper)
    sensitive_value=np.median(x)
    quality=np.array([0 for _ in range(nbins)], dtype='float32')
    for i in range(len(quality)):
        quality[i]=min(sum(x_clipped<=bins[i]), sum(x_clipped>=bins[i]))
    likelihoods=np.exp(epsilon*quality)/2
    probabilities=likelihoods/sum(likelihoods)

    flag=np.random.uniform(low=0, high=1)<np.cumsum(probabilities)
    DPrelease=min(bins[flag])
    return {'release':DPrelease, 'true':sensitive_value}

  
def generate_and_save_histogram (filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv",
                                 label='age',
                                 epsilon=1,
                                 measure='Mean',
                                 selection='age',
                                 high=160,
                                 low=0):
    #filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv"
    print('called generate_and_save_histogram')
    upper=high
    if measure=='Median':
        PUMSdata=pandas.read_csv(filepath)
        data=np.array(PUMSdata[selection], dtype='float32')
        populationTrue=float(np.median(data))
        sample_index=np.random.choice(range(1, len(data)+1, 1), size=100, replace=False)
        x=data[sample_index]
        n_sims=2000
        history=[None for _ in range(n_sims)]
        for i in (range(n_sims)):
            history[i]=medianRelease(x=x, lower=low, upper=high, epsilon=1)['release']

        x_clipped=clip(x, lower=low, upper=high)
        breaks=np.arange(0.5, upper+1)
        fig, axs=plt.subplots(2, 1)
        axs[0].hist(x_clipped, bins=breaks)
        axs[0].set_title('Histogram of Private Data')
        axs[0].axvline(x=np.median(x_clipped), color='r')
        axs[1].hist(history, bins=breaks)
        axs[1].set_title('Histogram of released DP medians')
        name='static/images/Laplace'+str(time.time())+'.png'
        plt.savefig(name)
        plt.show()
        plt.close()
        print('fig saved')
        return name

    else:
        print('measure given : '+measure+' hence using: Mean')
        PUMSdata=pandas.read_csv(filepath)
        data=np.array(PUMSdata[selection], dtype='float32')
        count=0
        release=[None for _ in range(2000)]
        true=[None for _ in range(2000)]
        print('Initialized empty lists')
        print('using epsilon', epsilon)
        for k in range(2000):
            DPmean=meanDP(x=data, lower=low, upper=high, epsilon=epsilon)
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
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('home.html')
@app.route('/home_with_logout')
def home_with_logout():
    logout_user()
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')
        
@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', UPLOAD_STATUS='CLICK TO UPLOAD')

@app.route('/upload_process', methods=['GET','POST'])
def upload_process():
    session['filename']=None
    print(request.method)
    print(request.data)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('upload.html', UPLOAD_STATUS='CLICK TO UPLOAD')
        file = request.files['file']
        # if file.filename=='':
        #     flash('No selected file')
        #     filepath="https://raw.githubusercontent.com/privacytoolsproject/cs208/master/data/FultonPUMS5full.csv"
        #     df=pandas.read_csv(filepath)
        #     headers_list=list(df)
        #     session['headers_list']=headers_list
        #     OPTIONS_LIST=list_to_html(headers_list)
        #     print(len(df[headers_list[0]]),'rows')
        #     print(OPTIONS_LIST)
        #     return render_template('upload.html', UPLOAD_STATUS='No File Selected', OPTIONS_LIST=OPTIONS_LIST)
        if file and allowed_file(file.filename):
            print('File is Allowed', file.filename)
            session['filename']=secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, session.get('filename')))
            df = pandas.read_csv(os.path.join(UPLOAD_FOLDER, session.get('filename')))
            headers_list=list(df)
            print(headers_list)
            session['headers_list'] = headers_list
            OPTIONS_LIST=list_to_html(headers_list)
            return render_template('upload.html', UPLOAD_STATUS='UPLOADED!', OPTIONS_LIST=OPTIONS_LIST)
        flash('only txt and csv allowed, Try Again!')
        return render_template('upload.html', UPLOAD_STATUS='WrongExtension, Try a csv or txt')

@app.route('/query_upload_process', methods=['GET','POST'])
def query_upload_process():
    #session['filename_query']=None
    print(request)
    print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return render_template('upload.html', UPLOAD_STATUS='CLICK TO UPLOAD')
        file = request.files['file']
        if file.filename=='':
            flash('No selected file')
            filepath="src/data.txt"
            df=pandas.read_csv(filepath)
            headers_list=list(df)
            session['headers_list']=headers_list
            TABS_LIST=query_src.list_to_html_tabs(headers_list)
            DIVS_TABS_LIST=query_src.list_to_html_divs_tabs(headers_list)
            return render_template('query.html', UPLOAD_STATUS='No File Selected', TABS_LIST=TABS_LIST, DIVS_TABS_LIST=DIVS_TABS_LIST)
        if file and allowed_file(file.filename):
            session['filename_query']="data.txt"
            file.save("src/data.txt")
            df = pandas.read_csv(os.path.join(UPLOAD_FOLDER, session.get('filename')))
            headers_list=list(df)
            session["headers_list"]=headers_list
            TABS_LIST=query_src.list_to_html_tabs(headers_list)
            DIVS_TABS_LIST=query_src.list_to_html_divs_tabs(headers_list)
            return render_template('query.html', UPLOAD_STATUS='UPLOADED!', TABS_LIST=TABS_LIST, DIVS_TABS_LIST=DIVS_TABS_LIST)
        flash('only txt and csv allowed, Try Again!')
        return render_template('query.html', UPLOAD_STATUS='WrongExtension, Try a txt')


    
@app.route('/process', methods=['GET','POST'])
def process():
    print(request)
    print(dict(request.args))
    e = request.args.get('e','0.1')
    d = request.args.get('d', '0.1')
    low = (request.args.get('low', '0'))
    high =  (request.args.get('high', '160'))
    low = get_float(low, 0)
    high = get_float(high, 160)
    try:
        selection_index = int(request.args.get('selection', '0'))-1
    except:
        selection_index=-1
    if selection_index == -1:
        selection = 'age'
    else:
        selection = session['headers_list'][selection_index]

    print('Selection being', selection)

    try:
        measure_index = int(request.args.get('measure', '0'))-1
    except:
        measure_index = -1
    if measure_index == -1:
        measure = 'Mean'
    else:
        measure = ['Mean', 'Median', 'Mode'][measure_index]


    try:
        epsilon=float(e)
    except:
        print('could not convert given epsilon to float')
        epsilon=0.1
    if session.get('filename')!=None:
        filepath = 'static/uploaded/'+session.get('filename')
        UPLOAD_STATUS='UPLOADED!'
        name=generate_and_save_histogram(filepath=filepath, epsilon=epsilon, measure=measure, selection=selection, low=low, high=high)
    else:
        UPLOAD_STATUS='USED DEFAULT FILE'
        name=generate_and_save_histogram(epsilon=epsilon, measure=measure, selection=selection, high=high, low=low)
    
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

@app.route('/query', methods=['GET','POST'])
def query():
    return render_template('query.html', UPLOAD_STATUS='Click to Upload')

@app.route('/query_save_process', methods=['GET', 'POST'])
def query_save_process():
    item=request.args.get('item','')
    item_text = request.args.get('item_text', '')
    print('item_text was ', item_text)
    query_src.save_item_text(item, item_text)
    return item_text

@app.route('/query_process', methods=['GET','POST'])
def query_process():
    #Processing args
    e=request.args.get('e', '0.1')
    low=request.args.get('low', '0')
    high=request.args.get('high', '125')
    qid=request.args.get('qiid', '(0,1)')
    dpid=request.args.get('dpid', '3')

    epsilon=get_float(e, 0.1)
    low = get_float(low, 0)
    high = get_float(high, 125)
    qid = tuple(qid)
    #TODO- Handle exception if input not tuple-like
    dpid = get_natural(dpid, 3)

    f = open("src/kwargs.txt", 'w+')
    f.write(str([qid,  dpid]))
    f.close()

    print(request)
    print(dict(request.args))
    try:
        filename_query=session.get('filename_query')
        UPLOAD_STATUS='UPLOADED'
    except:
        filename_query=None
        UPLOAD_STATUS='USED DEFAULT'

    f = open("src/attribute.txt", 'w+')
    f.write(str(session["headers_list"]))
    f.close()

    subprocess.call("src/K_Anonymity.py", shell=True)

    name=str(time.time())+'.txt'
    address = "static/css/"+name
    f = open(address, 'w+')
    f.close()
    shutil.copy2("src/Anonymity.txt", address)

    DOWNLOAD_PART = query_src.show_download_part(name)

    return render_template('query.html', UPLOAD_STATUS=UPLOAD_STATUS, DOWNLOAD_PART=DOWNLOAD_PART)

@app.route('/federatedML', methods=['GET', 'POST'])
@login_required
def federatedML():
    return render_template('federatedML.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login_page():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('login.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    print (request.form)
    username = request.form.get('username', '')
    print(username)
    password = request.form.get('password', '')
    remember = request.form.get('remember', False)
    print('username', username, 'password', password, 'remember', remember)
    if current_user.is_authenticated:
        print('already authenticated user')
        return render_template('index.html')
    elif username=='':
        print('empty username')
        return render_template('home.html')
    else:
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            print('Wrong password')
            return 'Wrong Username-Password Combination'
        login_user(user, remember = bool(remember))
        next_page = request.form.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            print('returning index')
            return render_template('index.html')
        print('next_page was ', next_page)
        return redirect(next_page)

@app.route('/check_username_available', methods=['GET', 'POST'])
def check_username_available():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user is not None and user.username is not None:
        print(user.username)
        return 'Please use a different Username'
    return ''

@app.route('/check_email_available', methods=['GET', 'POST'])
def check_email_available():
    value = request.args.get('email')
    user = User.query.filter_by(email=value).first()
    print(user)
    if user is not None and user.email is not None:
        print(user.email)
        return 'Please use a different email'
    return ''

@app.route('/register', methods=['GET', 'POST'])
def register():
    print('Args at register')
    print(request.args)
    print(request.form)
    print('request type:---->', request.method)
    username = request.args.get('username')
    password = request.args.get('password')
    remember = request.args.get('remember')
    email = request.args.get('email')
    ###Check if duplicate
    user = User.query.filter_by(username=username).first()

    if user is not None and user.username is not None:
        print(user.username)
        return 'Please use a different Username'
    if email == '':
        return 'Please enter a valid email'
    user = User.query.filter_by(email=email).first()
    if user is not None and user.username is not None:
        return 'Please use a different email address'

    user = User(username=username, email=email)
    print('Adding New User')
    print('username==', username)
    print('password==', password)
    print('remember==', remember)
    print('email==', email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return render_template('index.html')

@app.route('/joinFederatedProject', methods=['GET', 'POST'])
def joinFederatedProject():
    ProjectID = request.args.get('ProjectID')

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
	

app.secret_key = 'super secret key'
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'
login = LoginManager(app)
login.login_view = 'login_check'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return 'User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project():
    pass

@login.user_loader
def load_user(id): #app/models.py
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)