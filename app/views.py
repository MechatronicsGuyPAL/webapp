from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db
from .models import CDA

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    if request.method == "GET":
        return render_template('index.html',title='Home')

    elif request.method == "POST":
        return redirect(url_for('history'))

@app.route('/history', methods=['GET', 'POST'])
def history():

    entries=CDA.query.filter(CDA.id>1).limit(5).all()   

    if request.method == "GET":
        return render_template('history.html',title='history',val=0,item=entries[val])

    elif request.method == "POST":
        if request.form['selection']=='Yes':
            val+=1
            return render_template('history.html',title='history',item=entries[val])

        elif request.form['selection']=='No':
            return render_template('history.html',title='history',item=entries[val])

