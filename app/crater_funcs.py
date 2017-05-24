from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from .models import CDA
from datetime import datetime
from sqlalchemy import desc


class craterfunc:
    def get_attributes(self, entries):
        x1 = entries.x1
        x2 = entries.x2
        y1 = entries.y1
        y2 = entries.y2

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
        return dict( width = int(width), height = int(height), x_val = int(x_val), y_val = int(y_val), zoom = float(zoom), x1=x1, x2=x2, y1=y1, y2=y2 )

    def get_new_attributes(self, entries, clickX, clickY):
        x1 = entries.x1
        x2 = entries.x2
        y1 = entries.y1
        y2 = entries.y2

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

        shiftX = int(((float(200 - clickX))/200.0)*width_raw)
        shiftY = int(((float(200 - clickY))/200.0)*width_raw)
        #newX = center_x - int(shiftX*width_raw)
        #newY = center_y + int(shiftY*width_raw)
        newX = center_x - shiftX
        newY = center_y + shiftY
        new_x_val = newX - scale_xy*width_raw
        new_y_val = newY - scale_xy*height_raw

        x1_new = x1 - int(0.5*(float(shiftX)))
        x2_new = x2 - int(0.5*(float(shiftX)))
        y1_new = y1 + int(0.5*(float(shiftY)))
        y2_new = y2 + int(0.5*(float(shiftY)))
        print 'x1: ', x1
        print 'x2: ', x2
        print 'y1: ', y1
        print 'y2: ', y2
        print 'shiftX: ', shiftX
        print 'shiftY: ', shiftY
        print 'x1_new: ', x1_new
        print 'y1_new: ', y1_new
        print 'x2_new: ', x2_new
        print 'y2_new: ', y2_new

        return dict( width = int(width), height = int(height), x_val = int(new_x_val), y_val = int(new_y_val), zoom = float(zoom), x1=x1_new, x2=x2_new, y1=y1_new, y2=y2_new )



    def update_count(self, entry_field,entries):

        if entry_field == "yes":
            temp = "y"
        elif entry_field == "no":
            temp = "n"
        elif entry_field == "unsure":
            temp = "u"
        UserVote = models.Vote(crater_id = entries.id, vote_result = temp, start_timestamp = entries.timestamp, end_timestamp = datetime.utcnow() )
        db.session.add(UserVote)
        temp = entries.votes + 1
        entries.votes = temp
        db.session.add(entries)
        db.session.commit()
        db.session.remove()

    def query_database(self):
        entries = CDA.query.filter(CDA.score >= 0.09).order_by(CDA.timestamp).limit(1).first()
        entries.timestamp = datetime.utcnow()
        db.session.add(entries)
        db.session.commit()
        #entries = CDA.query.filter(CDA.id >1).limit(1).first()
        return entries



