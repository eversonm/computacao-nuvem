import jinja2
import pandas as pd
import pdfkit
from dynAccess import *
from datetime import datetime

def save_report(df):

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "templates/model.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    outputText = template.render(df=df)
    html_file = open('templates/reportds.html', 'w')
    html_file.write(outputText)
    html_file.close()
    relatorio = 'reports/relatorio_'+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+'.pdf'
    pdfkit.from_file('templates/reportds.html', relatorio)