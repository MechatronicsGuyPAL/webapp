#!flask/bin/python
from app import db, models


#known issue, in python, boolean valuse stored as "False/True", but json reads boolean as "false/true". in order to import the json, use a find and replace on the file to alter the text.

#set value depending on whether the JSON file is being used for the web app
#or if it is for use with the CDA. 
webapp = True


print('starting query')
entries = models.CDA.query.all()
first_flag = True
new_image_flag = True
imagestring = 'none'





print('creating JSON')
# open JSON file to write crater windows to
if webapp == True:
    jsonfile = open('data/jsons/webapp_data_V2.json','w')
else:
    jsonfile = open('data/jsons/CDA_training_data.json','w')

#one decimal format string
one_decimal = "{0:0.1f}"
# write the opening parentheses to the file
jsonfile.write('[')

for i, val in enumerate(entries):
    print('processing record #:{}'.format(i))
    score = entries[i].score
    x1 = entries[i].x1
    x2 = entries[i].x2
    y1 = entries[i].y1
    y2 = entries[i].y2
    GT_conflict = entries[i].GT_conflict
    var2 = entries[i].var2

    #check if current entry is the same image as previous entry
    if imagestring != entries[i].image:
            if first_flag != True:
                jsonfile.write('\n]\n}')
                jsonfile.write(',')
            first_flag = False
            new_image_flag = True
            imagestring = entries[i].image
            jsonfile.write('\n{{\n"image_path": "{}",\n"rects": ['.format(imagestring))

    if new_image_flag != True:
        jsonfile.write(',')
    new_image_flag = False


    jsonfile.write('\n{\n')
    jsonfile.write('"score": {},\n'.format(score))
    jsonfile.write('"x1": {}.0,\n'.format(x1))
    jsonfile.write('"x2": {}.0,\n'.format(x2))
    jsonfile.write('"y1": {}.0,\n'.format(y1))
    jsonfile.write('"y2": {}.0,\n'.format(y2))
    if webapp == True:
        jsonfile.write('"GT_conflict": {},\n'.format(GT_conflict))
        jsonfile.write('"IOU": {}\n'.format(var2))
    jsonfile.write('}')

jsonfile.write('\n]\n}\n]')
