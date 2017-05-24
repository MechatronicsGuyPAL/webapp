from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from .models import CDA
from datetime import datetime
from sqlalchemy import desc
import crater_funcs

@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == "GET":
        return render_template('index.html',title='Home')

    elif request.method == "POST":
        return redirect(url_for('crater', new_entry_flag = 1))


@app.route('/history', methods=['GET', 'POST'])
def history():


    if request.method == "GET":
        return render_template('history.html',title='history')

    elif request.method == "POST":
       return render_template('history.html',title='history')



@app.route('/crater', methods=['GET', 'POST'])
def crater():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        if request.args.get('new_entry_flag') is None:
            new_entry_status = 1
        else:
            new_entry_status = int(request.args.get('new_entry_flag'))


        if new_entry_status == 1:
            print new_entry_status
            entries = CF.query_database()
            attributes=CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        if new_entry_status == 0:
            print new_entry_status
            tempID = int(request.args.get('numID'))
            entries=models.CDA.query.get(tempID)
            attributes=CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)



    elif request.method == "POST":
        tempID = request.form.get(('numID'), type = int)
        entries=models.CDA.query.get(tempID)

        if request.form['selection']=='Yes':
            CF.update_count("yes", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='No':
            CF.update_count("no", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Unsure':
            CF.update_count("unsure", entries)
            entries = CF.query_database()
            attributes = CF.get_attributes(entries)
            return render_template('crater.html',title='crater',item=entries, attributes = attributes)

        elif request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            entries=models.CDA.query.get(tempID)
            attributes = CF.get_attributes(entries)
            return redirect(url_for('update_coords',numID=tempID))


@app.route('/update_coords', methods=['GET', 'POST'])
def update_coords():
    CF=crater_funcs.craterfunc()

    if request.method == "GET":
        tempID = int(request.args.get('numID'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_attributes(entries)
        return render_template('update_coords.html',title='update_coords',item=entries, attributes = attributes)


    elif request.method == "POST":
        if request.form['recenter_status']=='cancel':
            tempID = request.form.get(('numID'), type = int)
            entries=models.CDA.query.get(tempID)
            attributes=CF.get_attributes(entries)
            return redirect(url_for('crater', new_entry_flag = 0, numID=tempID))

        elif request.form['recenter_status']=='submit':
            relativeX = request.form.get(('relX'), type = int)
            relativeY = request.form.get(('relY'), type = int)
            tempID = request.form.get(('numID'), type = int)
            #entries=models.CDA.query.get(tempID)
            #attributes=CF.get_new_attributes(entries, relativeX, relativeY)
            return redirect(url_for('update_confirm',numID=tempID, relx = relativeX, rely = relativeY))


@app.route('/update_confirm', methods=['GET', 'POST'])
def update_confirm():
    CF=crater_funcs.craterfunc()


    if request.method == "GET":
        print "update cinfirm get request"
        tempID = int(request.args.get('numID'))
        relativeX = int(request.args.get('relx'))
        relativeY = int(request.args.get('rely'))
        entries=models.CDA.query.get(tempID)
        attributes=CF.get_new_attributes(entries, relativeX, relativeY)
        return render_template('update_confirm.html',title='update_confirm',item=entries, attributes = attributes)


    elif request.method == "POST":
        if request.form['selection']=='Re-Center':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('update_coords',numID=tempID))

        elif request.form['selection']=='Confirm':


            return redirect(url_for('crater', new_entry_flag = 1))



        elif request.form['selection']=='Cancel':
            tempID = request.form.get(('numID'), type = int)
            return redirect(url_for('crater', new_entry_flag = 0, numID=tempID))


