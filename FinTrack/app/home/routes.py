# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import razorpay
from bs4 import BeautifulSoup
import requests


client = razorpay.Client(auth=("rzp_test_ui6SHylFxya3wB","mfDawSJMdh75En9EP7xMDZlH"))

@blueprint.route('/index')
@login_required
def index():
    return render_template('my-projects.html', segment='index')

@blueprint.route('/colab', methods = ['GET', 'POST'])
def colab():
    invoice = ['item', 'quantity', 'rate', 'tax']
    invoices = []
    invoice_input = []
    for i in range(5):
        invoices.append([j+str(i) for j in invoice])
    if request.form:
        name = []
        first = request.form['First_Name']
        last = request.form['Last_Name']
        name.append(first)
        name.append(last)
        email = request.form['Email_Address']
        invoice_name = request.form['invoice_name']
        invoice_date = request.form['invoice_date']
        for i in invoices:
            invoice_input.append([request.form[i[j]] for j in range(4)])
        subtotal = []
        for i in invoice_input:
            subtotal.append((int(i[1]) * int(i[2])) + (int(i[2]) * (int(i[3]) / 100)))
        total = sum(subtotal)
        return render_template('invoice.html', segment='ui_maps',first=first,name=name,email=email,invoice_name=invoice_name, invoice_date=invoice_date, invoice_input=invoice_input, subtotal=subtotal ,total=total)
    return render_template('collaborate.html', segment='ui_maps', invoices=invoices)

@blueprint.route('/analysis', methods = ['GET', 'POST'])
def analysis():
    source = requests.get('https://socialstats.info/report/ashishchanchlani/instagram').text

    soup = BeautifulSoup(source,'lxml')
    article = soup.find('div',class_='d-flex')
    head = article.find_all('p', class_='report-header-number')
    y=[]
    for i in head:
        x = i.text
        if " " in x:
            x=x.split()[0]
        y.append(x)
    
    source = requests.get('https://www.speakrj.com/audit/report/viratkohli/facebook').text

    soup = BeautifulSoup(source,'lxml')
    article = soup.find('div',class_='justify-content-around')
    print(article.prettify())
    head = article.find_all('p', class_='report-header-number')
    fb=[]
    # z=[]
    for i in head:
        x = i.text
        if " " in x:
            x=x.split()[0]
        fb.append(x)
    
    source = requests.get('https://www.speakrj.com/audit/report/ashchanchlani/twitter').text

    soup = BeautifulSoup(source,'lxml')
    article = soup.find('div',class_='d-flex')
    head = article.find_all('p', class_='report-header-number')
    tw=[]
    for i in head:
        x = i.text
        if " " in x:
            x=x.split()[0]
        tw.append(x)
    return render_template('index.html', y = y, fb = fb, tw = tw, segment='index',)

@blueprint.route('/pay', methods = ['GET', 'POST'])
def pay():
    name_of_event = 'example'
    target_amount = 200 * 100
    payment = client.order.create({'amount' : target_amount, 'currency' : 'INR', 'payment_capture' : '1'})
    event_details = [name_of_event]
    if request.form:
        name_of_event = request.form['event_name']
        target_amount = int(request.form['target_amount']) * 100
        payment = client.order.create({'amount' : target_amount, 'currency' : 'INR', 'payment_capture' : '1'})
        event_details = [name_of_event]
        return render_template('fund-raiser.html',event_details=event_details,payment=payment)
    return render_template('fund-raiser.html',event_details=event_details,payment=payment, segment="ui_tables")

@blueprint.route('/success', methods = ['GET', 'POST'])
def success():
    return render_template('includes/success.html')



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
