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
        return dict( width = int(width), height = int(height), x_val = int(x_val), y_val = int(y_val), zoom = float(zoom) )

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


        shiftX = ((float(200 - clickX))/200.0)
        shiftY = ((float(200 - clickY))/200.0)
        newX = center_x - int(shiftX*width_raw)
        newY = center_y + int(shiftY*width_raw)
        new_x_val = newX - scale_xy*width_raw
        new_y_val = newY - scale_xy*height_raw

        print clickX
        print clickY
        print shiftX
        print shiftY

        return dict( width = int(width), height = int(height), x_val = int(new_x_val), y_val = int(new_y_val), zoom = float(zoom) )


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
        print entries.timestamp
        entries.timestamp = datetime.utcnow()
        print entries.timestamp
        db.session.add(entries)
        db.session.commit()
        #entries = CDA.query.filter(CDA.id >1).limit(1).first()
        print entries
        print "query finished"
        return entries
