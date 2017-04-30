
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
        return redirect(url_for('crater'))


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
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2        

        scale_xy = 1.0
        scale_wh = 2.0
        width_raw = x2 - x1
        height_raw = y2 - y1
        center_x = x2-(0.5*width_raw)
        center_y = y2-(0.5*height_raw)
        x_val = center_x - scale_xy*width_raw
        y_val = center_y - scale_xy*height_raw
        width = scale_wh*width_raw
        height = scale_wh*height_raw
        zoom_raw = 400.0/(float(width))
        zoom = round(zoom_raw, 2)
        print x1, x_val, x2, width_raw, width, center_x
        return dict( width = int(width), height = int(height), x_val = int(x_val), y_val = int(y_val), zoom = float(zoom) )
        #return dict( width = int(width_raw), height = int(height_raw), x_val = int(x1), y_val = int(y1), zoom = float(zoom))


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
            #entries = CDA.query.filter(CDA.id >1).limit(1).first()
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
