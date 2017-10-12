#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_

#change this field to contain the filename you want
file_name = 'finished_craters_10_10_17'




#WHAT IS F.WRITE SYNTAX?


print('starting query')
fin_craters = models.CDA.query.filter(models.CDA.vote_result != None).order_by(models.CDA.id)

#open file and write fields followed by recursively writing the crater entries
print('writing csv document')
file_path = 'data/csvs/'+file_name
f = open(file_path,'w')
f.write('id,image,x1,y1,x2,y2,score,IOU,vote_result,votes,votes_yes,votes_no,votes_unsure,votes_recenter,votes_SU,recenter_id,r_zscore,r_x1,r_y1,r_x2,r_y2')

for crater in fin_craters:
    rx1 = None
    ry1 = None
    rx2 = None
    ry2 = None
    r_zscore = None

    if crater.vote_result == 'recenter':
        recenter = models.Vote.query.get(crater.recenter_id)
        rx1 = recenter.x1_new
        ry1 = recenter.y1_new
        rx2 = recenter.x2_new
        ry2 = recenter.y2_new
        r_zscore = recenter.recenter_zscore

    f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(crater.id,
                                                                                    crater.image,
                                                                                    crater.x1,
                                                                                    crater.y1,
                                                                                    crater.x2,
                                                                                    crater.y2,
                                                                                    crater.score,
                                                                                    crater.IOU,
                                                                                    crater.vote_result,
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

f.close()
