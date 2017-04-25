
from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from .models import CDA
from datetime import datetime
from sqlalchemy import desc

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
       
        return render_template('history.html',title='history')


    #updates the yes counts for the query request
    elif request.method == "POST":
       return render_template('history.html',title='history')



@app.route('/crater', methods=['GET', 'POST'])
def crater():
    def get_attributes(self):
        width =  int(1.0*(self.x2 - self.x1))
        height = int(1.0*(self.y2 - self.y1))
        x_val = int(self.x1-int(0*width))
        y_val = int(self.y1-int(0*width))
        zoom_raw = 400.0/(float(width))
        zoom = round(zoom_raw, 2)
        return dict( width = int(width), height = int(height), x_val = int(x_val), y_val = int(y_val), zoom = float(zoom) )


    def update_count(entry_field, form_field,entries):
            temp = request.form.get((form_field), type = int)
            if entry_field == "yes":
                entries.yes = (temp + 1)
            elif entry_field == "no":
                entries.no = (temp + 1)
            elif entry_field == "unsure":
                entries.unsure = (temp + 1)
            entries.timestamp = datetime.utcnow()
            db.session.add(entries)
            db.session.commit()
            db.session.remove()

    def query_database():
            entries = CDA.query.filter(CDA.score >= 0.09).order_by(CDA.timestamp).limit(1).first()
            return entries


    if request.method == "GET":
        entries = query_database()
        attributes = get_attributes(entries)
        return render_template('crater.html',title='crater',item=entries, attributes = attributes)

    elif request.method == "POST":
        tempID = request.form.get(('numID'), type = int)
        entries=models.CDA.query.get(tempID)

        if request.form['selection']=='Yes':
            update_count("yes", "yescount", entries)
            entries = query_database()
            attributes = get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='No':
            update_count("no", "nocount", entries)
            entries = query_database()
            attributes = get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Unsure':
            update_count("unsure", "unsurecount", entries)
            entries = query_database()
            attributes = get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)
