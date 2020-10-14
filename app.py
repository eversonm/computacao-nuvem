from flask import Blueprint, Flask, request , abort , redirect , Response ,url_for, render_template
from flask_login import LoginManager , login_required , UserMixin , login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine
from pgconn import POSTGRES
from mariadbconn import mysql
from graphspython import *
from s3folder import upload_dir_s3
from html_reports import save_report
from dynamo import *
from datetime import datetime
import os
import sys
import boto3
import glob 
import re
import pdfkit
import jinja2

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

auth = Blueprint('auth', __name__)
app.register_blueprint(auth)

############################Usuarios############################
class User(UserMixin,db.Model):
    # ...
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))


name_f = {
    "name":""
}

data_infor = {
    "nome_arq":"",
    "dataset_info":""
}
messages = {
    "m":""
}
tags = [
        'gpu',
        'tpu',
        'beginner',
        'data visualization',
        'business',
        'exploratory data analysis',
        'deep learning',
        'classification',
        'utility script',
        'earth and nature',
        'arts and entertainment',
        'computer science',
        'feature engineering',
        'internet',
        'data cleaning',
        'education',
        'clothing and accessories',
        'online communities',
        'nlp',
        'health'
]
graphs = ["barra","barrah","linha","histograma","boxplot","setores","scatterplot","scattergeo", "linha-ano", "linha-mes"]
api = KaggleApi()
api.authenticate()

@app.before_first_request
def create_tables():
    db.create_all()

def create_table_query(owner = 'everson', dataset_name = 'malware', namefile="file.csv"):
    RX = re.compile('([-/=+!$@#¨%&*.,;:()])')
    description = api.metadata_get(owner_slug=owner,dataset_slug=dataset_name)
    for item in description['data']:
        if item['name']==namefile:
            description = item
            break
    df_name = str('_')+description['name'].replace('.csv','_')
    df_name = RX.sub('', df_name)
    df_name = df_name.replace('[','').replace(']','')
    
    query = "CREATE TABLE IF NOT EXISTS "+df_name+' ('
    
    for item in description['columns']:
        if item['type']=='String':
            item.update({'type':'varchar'})
        if item['type']=='DateTime':
            item.update({'type':'date'})
        if item['type']=='Uuid':
            item.update({'type':'real'})
        if item['type']=='None':
            item.update({'type':'varchar'})
        if item['type']==None:
            item.update({'type':'varchar'})
        item_n = RX.sub('', item['name'])
        query = query+' '+'_'+str(item_n.replace(' ','_'))+'_ '+str(item['type'])+','
        query = query.replace('[','').replace(']','')
    query = query[:-1]
    query = query+' )'
    print(query)
    return {'table_name': df_name, 'query':query}

def execute_query_create_table(query):
    db_string = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    db = create_engine(db_string)
    try:
        db.execute(query)
    except:
        print("Error")

def insertDB(arquivo = '1.csv', tabela = 'usuarios'):
    with open(arquivo, 'r') as f:
        first_line = f.readline()    
        conn = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES).raw_connection()
        cursor = conn.cursor()
        cmd = "COPY "+tabela+" FROM STDIN DELIMITER ',' CSV;"
        try:
            cursor.copy_expert(cmd, f)
            print("Inserido no Banco com Sucesso!")
        except:
            cursor.execute("rollback")
        
        conn.commit()

def bytesto(bytes):
    bsize=1024
    a = 2
    r = float(bytes)
    for i in range(a):
        r = r / bsize

    #return(r)
    return ("%.2f" % r)                           
############################ENDPOINTS############################

#######################Pagina Inicial############################
@app.route('/')
def index():
    return render_template('index.html')

#########################Pagina Home#############################
@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    tag_id = request.form.get("newtag")
    search_tag = request.form.get("searchtag")
    thread = api.datasets_list(tagids=tag_id, page=1, search=search_tag, async_req=True, filetype='csv')
    get_ref = thread.get()

    if request.form.get("info"):
        data_info=request.form.get("info")
        return redirect(url_for('.information', messages=data_info))
        #return render_template("app.html", dataset_name=dataset_name)
        #return redirect("/application")
    return render_template("home.html", tags=tags, get_ref=get_ref)

@app.route('/information', methods=["GET", "POST"])
@login_required
def information():
    from bs4 import BeautifulSoup
    atrib = request.args['messages']
    messages.update({"m":atrib})
    data_info = atrib
    
    owner, dataset_name = data_info.split('/')
    thread = api.metadata_get(owner_slug=owner,dataset_slug=dataset_name, async_req=True)
    
    description = thread.get()
    summ = 0
    for item in description['data']:
        summ = summ + item['totalBytes']

    description['data'][0]['totalBytes'] = bytesto(summ)
    description['description'] = BeautifulSoup(description['description'], 'html.parser')
    
    horarioacesso = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    link = "www.kaggle.com/"+data_info
    nometabela = description['title']
    dynamodb_post(nome=nometabela, horario=horarioacesso, link=link)
    if request.form.get("baixar"):
        owner, dataset_name = data_info.split('/')
        os.system("mkdir "+'datasets/'+str(dataset_name))
        path = 'datasets/'+str(dataset_name)
        api.dataset_download_files(dataset=data_info, unzip=True, path=path)
        # importar dataset para s3
        upload_dir_s3()
        return redirect(url_for('.list_files', messages=data_info))
    return render_template("information.html", description=description)
#######################listagem Arquivos##########################
@app.route('/list_files', methods=["GET","POST"])
@login_required
def list_files():

    atrib = request.args['messages']
    data_info = atrib
    owner, dataset_name = atrib.split('/')

    path = './datasets/'+str(dataset_name)+'/'
    files = glob.glob(path + '**/*', recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    if request.form.get("nfile"):
        name_ = request.form.get("nfile")
        print(name_)
        data_infor.update({"nome_arq": name_})
        data_infor.update({"dataset_info": data_info})
        return redirect(url_for('.application', nfile=name_, messages=atrib))
    return render_template("listfiles.html", files=files)

###########################Aplicacao##############################
@app.route('/application', methods=["GET","POST"])
@login_required
def application():

    name_file = data_infor["nome_arq"]
    returnlistfilesnow = messages["m"]
    #print(name_file)
    if name_file:
        name_f.update({"name":name_file})
        #print(name_f)
    attr1 = request.form.get('attr1')
    attr2 = request.form.get('attr2')
    tipo_grafico = request.form.get('attr3')

    dataframe = pd.read_csv(name_f["name"])
    dados = dataframe.head()

    if request.form.get("returnl"):
        return redirect(url_for('.list_files', messages=returnlistfilesnow))
        
    if request.form.get('savedb'):
        owner, dataset_name = data_infor['dataset_info'].split('/')
        table = create_table_query(owner=owner, dataset_name=dataset_name, namefile=name_f['name'].split("/")[-1])
        execute_query_create_table(table['query'])
        insertDB(arquivo = name_file, tabela=table['table_name'])
        return render_template("savedb.html")

    if (attr1 or attr2) and tipo_grafico:
        fig = pĺot_graphs_front(dataframe, attr1, attr2, tipo_grafico)
        return render_template("summary.html", tables=[dados.to_html(classes='data')], titles=dados.columns.values, fig=fig.show(), graphs=graphs)
    return render_template("summary.html", tables=[dados.to_html(classes='data')], titles=dados.columns.values, fig=None, graphs=graphs)

    #return render_template("summary.html", tables=[dados.to_html(classes='data')], titles=dados.columns.values)

###############################LOGIN#################################
@app.route('/login', methods=['POST', 'GET'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return render_template('login.html')

    if email and password:
        login_user(user, remember=remember)
        return render_template('profile.html')
    return render_template('login.html')

#############################REGISTER#################################
@app.route('/signup', methods=['POST', 'GET'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if email and user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return render_template('signup.html')

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return render_template('signup.html')

#############################Reports#################################
@app.route('/reports' , methods = ['GET' , 'POST'])
@login_required
def reports():
    df_ = dynamodb_get()
    df = pd.DataFrame(df_)
    df = df.sort_values(by=['horarioacesso'], ascending=False)
    if request.form.get("pdfsave"):
        save_report(df)
        return render_template('relatorio.html', df=df)

    return render_template('relatorio.html', df=df)

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #return redirect(url_for('.index'))
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return '<p>Você não efetuou login!</p><a href="/">Faça Login ou Cadastro aqui</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug =True)

#https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
#https://www.askpython.com/python/examples/list-files-in-a-directory-using-python
