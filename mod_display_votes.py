#!flask/bin/python
from app import db, models
from sqlalchemy import and_, or_
from operator import itemgetter
from collections import namedtuple
from pprint import pprint
import numpy as np
import cv2 as cv

#This module is intended to search through the list of finished craters, count the number of craters per image
#and print the resultant image name with the number of finished craters in ascending order.


#empty list to hold images's of finished craters
image_list = []
totals_list = []


#query CDA for all finished craters except those requireing a review
finished = models.CDA.query.filter(or_(models.CDA.vote_result == 'yes',models.CDA.vote_result == 'no', models.CDA.vote_result == 'recenter'))


print("generating image list")
for i, val in enumerate(finished):
    if not finished[i].image in image_list:
        image_list.append(finished[i].image)
image_len = len(image_list)
i=0
print("evaluating image list")
for image_entry in image_list:
    
    yes = 0
    no = 0
    recenter = 0
    total = 0
    available = 0
    fin_short = models.CDA.query.filter(and_(models.CDA.image == image_entry, models.CDA.IOU <= .25))
    for fin_entry in fin_short:
        available += 1
        if (fin_entry.vote_result == 'yes'):
            yes += 1
            total += 1
        elif (fin_entry.vote_result == 'no'):
            no += 1
            total += 1
        elif (fin_entry.vote_result == 'recenter'):
            recenter += 1
            total += 1
    image_craters = {
        "yes": yes,
        "no": no,
        "recenter": recenter,
        "total": total,
        "image_name": image_entry,
        "available": available
    }
    totals_list.append(image_craters)
    # print("Craters: {}, Yes: {}, No: {}, Re-Center: {}, Image: {}".format(
    #                                                                     totals_list[i]['total'],
    #                                                                     totals_list[i]['yes'],
    #                                                                     totals_list[i]['no'],
    #                                                                     totals_list[i]['recenter'],
    #                                                                     totals_list[i]['image_entry']
    #                                                                     ))

    print("Item {} out of {} finished".format((i+1),image_len))
    i += 1

#sort list in ascending order and print contents
print("Sorting list")
new_list = sorted(totals_list, key=itemgetter('total'), reverse = True) 
for y, val in enumerate(new_list):
    print("Craters: {}, Yes: {}, No: {}, Re-Center: {}, Image Name: {}, Total craters: {}".format(
                                                                        new_list[y]['total'],
                                                                        new_list[y]['yes'],
                                                                        new_list[y]['no'],
                                                                        new_list[y]['recenter'],
                                                                        new_list[y]['image_name'],
                                                                        new_list[y]['available']
                                                                        ))
# i_num = 0
# while (i_num < 10):    
    
#     print("drawing rectangle on {}".format(new_list[i_num]['image_name']))
#     rect_short = models.CDA.query.filter(and_(models.CDA.image == new_list[i_num]['image_name'], models.CDA.vote_result != None))
#     img_path_name = new_list[i_num]['image_name']
#     img_path, img_name = [str(s) for s in img_path_name.split('/')]
#     image_to_rect = 'app/static/' + img_path_name
#     image_to_write = 'data/images/result_' + img_name
    
#     img = cv.imread(image_to_rect)
#     i = 0
#     font = cv.FONT_HERSHEY_COMPLEX_SMALL
#     for rect in rect_short:
#         x1 = rect_short[i].x1
#         y1 = rect_short[i].y1
#         x2 = rect_short[i].x2
#         y2 = rect_short[i].y2
#         no_num = rect_short[i].results_no
#         yes_num = rect_short[i].results_yes
#         count_string = str(yes_num)+':'+str(no_num)+':'+str(rect_short[i].id)
#         if rect_short[i].vote_result == 'no':
#             B = 0
#             G = 0
#             R = 255
#         elif rect_short[i].vote_result == 'yes':
#             B = 0
#             G = 255
#             R = 0
#         else:
#             B = 0
#             G = 0
#             R = 0
#         i += 1

#         cv.rectangle(img, (x1, y1), (x2, y2), (B,G,R), 2)
#         cv.putText(img, count_string, (x1,y2),font,0.7,(B,G,R))
#         cv.putText(img, img_name, (50,50),font,0.7,(0,255,0))
#     cv.imwrite(image_to_write,img)
#     i_num += 1


