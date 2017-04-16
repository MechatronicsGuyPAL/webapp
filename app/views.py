

from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
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

    if request.method == "GET":
        entries=CDA.query.filter(CDA.id>1).limit(1).first()
        return render_template('history.html',title='history',item=entries)



    elif request.method == "POST":
        tempID = request.form.get(('numID'), type = int)
        entries=models.CDA.query.get(tempID)
        #entries=db.session.query(models.CDA).get(tempID)
        if request.form['selection']=='Yes':
            tempyes = request.form.get(('yescount'), type = int)
            entries.yes = (tempyes + 1)
            db.session.add(entries)
            db.session.commit()
            db.session.remove()
            entries=CDA.query.filter(CDA.id>1).limit(1).first()
            return render_template('history.html',title='history',item=entries)

        elif request.form['selection']=='No':
            return render_template('history.html',title='history',item=entries)

