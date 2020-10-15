# computacao-nuvem
Trabalho Final de Computação em Nuvem 2020.1 - UFC

## Python Requisitos
<a href="https://www.python.org/doc/versions/">
	<img src="https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?style=for-the-badge" alt="Python compatible versions" />
</a><br />

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Flask-Login](https://flask-login.readthedocs.io), [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), [Kaggle](https://www.kaggle.com/docs/api), [MySQL-Connector-Python](https://dev.mysql.com/doc/connector-python/en/), [Numpy](https://numpy.org/doc/1.19/), [Pandas](https://pandas.pydata.org/docs/), [PDFkit](https://pypi.org/project/pdfkit/), [Plotly](https://plotly.com/python/), [Psycopg2](https://www.psycopg.org/docs/)
---

## Recomendações para uso da aplicação
*Criar um ambiente usando python venv ou baixar e instalar o Miniconda*<br />

---

## Formas de instalar os pacotes
*Via Pip ou Conda*<br />
*Instalar também o wkhtmltopdf: $ sudo apt-get install wkhtmltopdf*<br />

---

### Pip install
*pip install beautifulsoup4 boto3 flask flask-login flask-sqlalchemy kaggle mysql-connector-python numpy pandas pdfkit plotly psycopg2 *<br />

---

### Conda install
*conda install beautifulsoup4 boto3 flask flask-login flask-sqlalchemy mysql-connector-python numpy pandas pdfkit plotly psycopg2*<br />
*conda install -c conda-forge kaggle*<br />
*conda install -c conda-forge python-pdfkit*<br />

---

### Ambiente em Nuvem - Amazon AWS
O trabalho foi desenvolvido utilizando uma conta no AWS Educate. Os serviços usados na aplicação foram: AWS API Gateway, AWS DynamoDB, AWS IAM, AWS Lambda, AWS RDS e o Amazon S3.

---

### Amazon API Gateway
*Necessário para acessar uma tabela do DynamoDB*<br />
*Definido um endpoint: <b>/mineração</b>*<br />
*Definido dois métodos: <b>GET</b> e <b>POST</b>*<br />
*GET realiza um Scan na tabela do DynamoDB, retornando todas as tuplas*<br />
*POST realiza uma inserção na tabela do DynamoDB*<br />

---

### Amazon DynamoDB
*Usado para geração de relatórios da aplicação*<br />
*Pode-se criar uma tabela com qualquer nome, mas com os seguintes atributos: nometabela, horarioacesso e link*<br />
*<b>nometabela</b>: nome do dataset acessado pela API do Kaggle*<br />
*<b>horarioacesso</b>: horário em que foi realizada uma consulta na API do Kaggle*<br />
*<b>link</b>: o link para acesso ao dataset no site do Kaggle*<br />

---

### Amazon IAM
*Usado para criação de uma Role para acessar a tabela do DynamoDB*<br />
*Também é necessário definir uma política para acessar os métodos do DynamoDB: getItem, Scan e putItem*<br />
*Deve-se criar um Model Schema para efetuar inserções na tabela do Dynamo. Disponível na pasta model-schema*<br />

---

### Amazon Lambda
*Duas funções são utilizadas para executar os métodos GET e POST*<br />
*Funções em NodeJS disponíveis na pasta lambda-functions*<br />
*Deve-se criar um Model Schema para efetuar inserções na tabela do Dynamo. Disponível na pasta Model Schema*<br />

---

### Amazon RDS
*Foram utilizadas duas instâncias de bancos de dados*<br />
*<b>Postgres</b>: salvar um arquivo .csv como uma tabela do banco*<br />
*<b>MariaDB</b>: usada para salvar as credenciais dos usuários*<br />

---

### Amazon S3
*Utilizado para salvar os objetos da aplicação*<br />
*Necessário criar um Bucket com duas pastas: <b>datasets</b> e <b>reports</b>*<br />
*<b>datasets</b>: salvar todos os datasets após a consulta realizada na apicação*<br />
*<b>reports</b>: salvar os relatórios de acesso a API do Kaggle*<br />

---