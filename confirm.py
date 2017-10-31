#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_
from datetime import datetime


#this module outputs csv files of the finished craters and the current votes to the webapp/data/csvs directory


#choose which databases to export, set to True to export, or False to skip
export_craters = True
export_votes = True

#change these fields to contain the filenames you want
crater_CSV_filename = 'no_conflict_craters'
votes_CSV_filename = 'default_votes_csv_filename'



#*************************************************
#       This code should not be altered
#*************************************************
#export crater CSV
if export_craters == True:

    print('starting predictions query')
    #fin_craters = models.CDA.query.filter(models.CDA.vote_result != None).order_by(models.CDA.id)
    fin_craters = models.CDA.query.filter(or_(models.CDA.var2 == 'yes',models.CDA.var2 == 'no',models.CDA.var2 == 'recenter'))
    #fin_craters = models.CDA.query.all()

    #open file and write fields followed by recursively writing the crater entries
    print('writing csv document')
    crater_file_path = 'data/csvs/'+crater_CSV_filename
    f_crater = open(crater_file_path,'w')
    f_crater.write('id,image,x1,y1,x2,y2,score,IOU,Var2 - vote_result,votes,votes_yes,votes_no,votes_unsure,votes_recenter,votes_SU,recenter_id,r_zscore,r_x1,r_y1,r_x2,r_y2\n')

    for crater in fin_craters:
        rx1 = None
        ry1 = None
        rx2 = None
        ry2 = None
        r_zscore = None



        f_crater.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(crater.id,
                                                                                        crater.image,
                                                                                        crater.x1,
                                                                                        crater.y1,
                                                                                        crater.x2,
                                                                                        crater.y2,
                                                                                        crater.score,
                                                                                        crater.IOU,
                                                                                        crater.var2,
                                                                                        crater.votes,
                                                                                        crater.results_yes,
                                                                                        crater.results_no,
                                                                                        crater.results_unsure,
                                                                                        crater.results_recenter,
                                                                                        crater.results_SU_vote,
                                                                                        crater.recenter_id,
                                                                                        r_zscore,
                                                                                        rx1,
                                                                                        ry1,
                                                                                        rx2,
                                                                                        ry2))

    f_crater.close()
