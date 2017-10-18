from flask import render_template, flash, session, g, request, url_for, redirect
from app import app, db, models
from .models import CDA
from datetime import datetime
from sqlalchemy import desc, and_


class craterfunc:
    def session_num(self):
        user_ip = str(request.remote_addr)
        try:
            first, second, third, fourth = [str(s) for s in user_ip.split('.')]
            ses_num = first + second + third
            print ses_num
            return ses_num
        except ValueError as e:
            print "Failed to get user ip"
            return "no_data"    



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
        if x_val <= 0:
            x_val = 0
        y_val = center_y - scale_xy*height_raw
        if y_val <= 0:
            y_val = 0
        width = scale_wh*width_raw
        height = scale_wh*height_raw
        zoom_raw = 400.0/(float(width))
        zoom = round(zoom_raw, 2)
        return dict( width = int(width), 
                    height = int(height), 
                    x_val = int(x_val), 
                    y_val = int(y_val), 
                    zoom = float(zoom), 
                    x1=x1, 
                    x2=x2, 
                    y1=y1,
                    y2=y2,
                    vote_result=entries.vote_result,
                    width_original = width_raw)

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
        if x_val <= 0:
            x_val = 0
        y_val = center_y - scale_xy*height_raw
        if y_val <= 0:
            y_val = 0
        width = scale_wh*width_raw
        height = scale_wh*height_raw
        zoom_raw = 400.0/(float(width))
        zoom = round(zoom_raw, 2)

        shiftX = int(((float(200 - clickX))/200.0)*width_raw)
        shiftY = int(((float(200 - clickY))/200.0)*width_raw)
        newX = center_x - shiftX
        newY = center_y + shiftY
        new_x_val = newX - scale_xy*width_raw
        if new_x_val <= 0:
            new_x_val = 0        
        new_y_val = newY - scale_xy*height_raw
        if new_y_val <= 0:
            new_y_val = 0

        x1_new = x1 - int(0.5*(float(shiftX)))
        x2_new = x2 - int(0.5*(float(shiftX)))
        y1_new = y1 + int(0.5*(float(shiftY)))
        y2_new = y2 + int(0.5*(float(shiftY)))

        return dict( width = int(width), 
                    height = int(height), 
                    x_val = int(new_x_val), 
                    y_val = int(new_y_val), 
                    zoom = float(zoom), 
                    x1=x1_new, 
                    x2=x2_new, 
                    y1=y1_new, 
                    y2=y2_new,
                    vote_result=entries.vote_result,
                    width_original = width_raw)


    def update_count(self, entry_field,entries):
        session_num = self.session_num()
        if entry_field == "yes":
            temp_entry = "yes"
            temp_yes = entries.results_yes + 1
            entries.results_yes = temp_yes
        elif entry_field == "no":
            temp_entry = "no"
            temp_no = entries.results_no + 1
            entries.results_no = temp_no            
        elif entry_field == "unsure":
            temp_entry = "unsure"
            temp_unsure = entries.results_unsure + 1
            entries.results_unsure = temp_unsure
        temp_vote = entries.votes + 1
        entries.votes = temp_vote
        db.session.add(entries)
        UserVote = models.Vote(crater_id = entries.id, 
                                vote_result = temp_entry, 
                                start_timestamp = entries.timestamp, 
                                end_timestamp = datetime.utcnow(),
                                session_data = session_num )
        db.session.add(UserVote)
        db.session.commit()
        db.session.remove()

    def query_database(self):
        test_val = .5
        entries = None
        time_since_flag = False
        while entries is None:
            test_val -= 0.05
            entries = CDA.query.filter(and_(CDA.IOU <= .25, CDA.score >= test_val, CDA.votes < 15, CDA.vote_result == None)).order_by(CDA.timestamp.desc()).limit(1).first()
            print("query, test val at {}".format(test_val))
            if ((entries is not None) and (self.query_time_since(entries) < 60)):
                    print("query time exceeded")
                    entries = CDA.query.filter(and_(CDA.IOU <= .25, CDA.score >= test_val, CDA.votes < 15, CDA.vote_result == None)).order_by(CDA.timestamp.desc()).limit(500)
                    for entry in entries:
                        print("checking entries")
                        if ((self.query_time_since(entry) >= 60) ):
                            time_since_flag = True
                            entries = entry
                            minutes = self.query_time_since(entry)
                            print("{} minutes since last query, IOU is {}".format(minutes, entries.IOU))
                            break
                    if time_since_flag == False:
                        entries = None

        entries.timestamp = datetime.utcnow()
        db.session.add(entries)
        db.session.commit()
        return entries

    def update_coords(self, entries, x1_new, x2_new, y1_new, y2_new):
        session_num = self.session_num()
        UserVote = models.Vote(crater_id = entries.id, 
                                vote_result = "recenter", 
                                start_timestamp = entries.timestamp, 
                                end_timestamp = datetime.utcnow(), 
                                x1_new = x1_new, 
                                x2_new = x2_new, 
                                y1_new = y1_new, 
                                y2_new = y2_new,
                                session_data = session_num )
        db.session.add(UserVote)
        temp_recenter = entries.results_recenter + 1
        entries.results_recenter = temp_recenter
        temp_vote = entries.votes + 1
        entries.votes = temp_vote
        db.session.add(entries)
        db.session.commit()
        db.session.remove()

    def query_time_since(self, entry):
        last_query = entry.timestamp
        current_query = datetime.utcnow()
        time_since = current_query - last_query
        minutes = (int(time_since.total_seconds())/60)
        return minutes

    def super_user_query(self):
            #entries = CDA.query.filter(and_(CDA.vote_result == None, CDA.score <= 0.36, CDA.score >= 0.34)).limit(1).first()
            try:
                #entries = CDA.query.filter(CDA.vote_result == 'review').order_by(CDA.score.desc()).limit(1).first()
                entries = CDA.query.filter(and_(CDA.vote_result == None, CDA.score <= 0.47, CDA.score >= 0.43,CDA.IOU <= .25)).limit(1).first()
                entries.timestamp = datetime.utcnow()
                db.session.add(entries)
                db.session.commit()
            except:
                entries = self.query_database()
            return entries


    def super_user_update_entry(self, entry_field,entries):
        session_num = self.session_num()
        if entry_field == "yes":
            temp_entry = "yes"
        elif entry_field == "no":
            temp_entry = "no"
        elif entry_field == "unsure":
            temp_entry = "review"
        if entries.results_SU_vote != None:
            temp_SU = entries.results_SU_vote + 1
        else:
            temp_SU = 1
        entries.vote_result = temp_entry
        entries.results_SU_vote = temp_SU
        entries.timestamp = datetime.utcnow()
        db.session.add(entries)
        UserVote = models.Vote(crater_id = entries.id, 
                                vote_result = temp_entry, 
                                start_timestamp = entries.timestamp, 
                                end_timestamp = datetime.utcnow(),
                                session_data = session_num,
                                vote_type = 'super_user_vote')
        db.session.add(UserVote)
        db.session.commit()
        db.session.remove()

    def super_user_update_coords(self, entries, x1_new, x2_new, y1_new, y2_new):
        session_num = self.session_num()
        UserVote = models.Vote(crater_id = entries.id, 
                                vote_result = "recenter", 
                                start_timestamp = entries.timestamp, 
                                end_timestamp = datetime.utcnow(), 
                                x1_new = x1_new, 
                                x2_new = x2_new, 
                                y1_new = y1_new, 
                                y2_new = y2_new,
                                session_data = session_num,
                                vote_type = 'super_user_vote')
        db.session.add(UserVote)
        if entries.results_SU_vote != None:
            temp_SU = entries.results_SU_vote + 1
        else:
            temp_SU = 1
        entries.results_SU_vote = temp_SU
        entries.vote_result = 'recenter'
        entries.timestamp = datetime.utcnow()
        db.session.add(entries)
        db.session.commit()
        db.session.remove()

