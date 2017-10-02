#!flask/bin/python
from app import db, models
#this script evaluates the collected votes and assigns the result status to the corresponding CDA entry

vote_list = []


votes = models.Vote.query.all()
finished_craters = 0
total_votes = 0

#get list of CDA ids from votes
for i, val in enumerate(votes):
    if not votes[i].crater_id in vote_list:
        vote_list.append(votes[i].crater_id)

#evaluate votes for each id in the list
for n, val in enumerate(vote_list):
    v_num = 0
    y_num = 0
    n_num = 0
    u_num = 0
    r_num = 0

    #count votes to make sure only completed entries are modified
    entries=models.CDA.query.get(vote_list[n])
    if entires.var1 == 'empty':
        for x, val in enumerate(votes):
            if votes[x].crater_id == vote_list[n]:
                v_num += 1
                if votes[x].vote_result == 'yes':
                    y_num +=1
                elif votes[x].vote_result == 'no':
                    n_num +=1
                elif votes[x].vote_result == 'unsure':
                    u_num +=1
                elif votes[x].vote_result == 'recenter':
                    r_num +=1


                    
        #record results
        if v_num >= 15:
            if (y_num >= 10):
                entries.var1 = 'yes'
            else if (n_num >= 10):
                entries.var1 = 'no'
            else if ( u_num >= 10):
                entries.var1 = 'unsure'
            else if (((y_num + r_num) >= 6) and (n_num >= 6)):
                entries.var1 = 'borderline'
            else if (((r_num + y_num) >= 10) and (r_num >= 5)):
                entries.var1 = 'recenter'
            else:
                entries.var1 = 'review'
            print("Crater ID {}: Vote result {}".format(entries.id, entries.var1))
            db.session.add(entries)
print('Committing vote results')
db.session.commit()

#determine appropriate recenter vote to use as the entry on "recenter" status CDA entries
recenters = models.CDA.query.filter(and_(CDA.var1 == 'recenter', CDA.var2 == 'empty'))
for i, val in enumerate(recenters):
    recenter_votes = models.Vote.query.filter(and_(Vote.crater_id == recenters[i].id, Vote.var1 == 'recenter'))

    num = 0.0
    total_x = 0.0
    total_y = 0.0
    mean_x = 0.0
    mean_y = 0.0
    varience_total_x = 0.0
    varience_total_y = 0.0
    stddev_x = 0.0
    stddev_y = 0.0
    z_score = 1000000.0
    recenter_id = 0

    for a, val in enumerate(recenter_votes):
        num += 1
        total_x += recenter_votes[a].x1_new
        total_y += recenter_votes[a].y1_new
    
    mean_x = (total_x/num)
    mean_y = (total_y/num)

    for b, val in enumerate(recenter_votes):
        varience_total_x += (recenter_votes[b].x1_new - mean_x)**2
        varience_total_y += (recenter_votes[b].y1_new - mean_y)**2

    stddev_x = ((varience_total_x/num)**0.5)
    stddev_y = ((varience_total_y/num)**0.5) 

#find the lowest combined z-score for the x y recenter votes, and assign that vote as the new location.
    for c, val in enumerate(recenter_votes):
        temp_zscore = (abs((recenter_votes[c].x1_new-mean_x)/stddev_x) + abs((recenter_votes[c].y1_new-mean_y)/stddev_y))
        if (temp_zscore < z_score):
            z_score = temp_zscore
            recenter_id = recenter_votes[c].id
            print('recenter crater ID: {}, to location ({},{}), combined z-score of {}'.format(recenter_votes[c].crater_id,
                                                                                                recenter_votes[c].x1_new,
                                                                                                recenter_votes[c].y1_new,
                                                                                                z_score))

    recenters[i].var2 = str(recenter_id)
    db.session.add(recenters[i])
print('Committing recenter location')
db.session.commit()

