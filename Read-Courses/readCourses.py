import json
from pprint import pprint
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object as ParseObject
from parse_rest.datatypes import ParseType, ParseResource
from datetime import datetime

APPLICATION_ID = "2yokKd96SUq3dKCQDcSI7LlGPJ7ZddnCMwbCIvX7"
REST_API_KEY = "MyfLxYfGm8iaxVahmsTCeKSNNuiz2wKzkQIOCyhS"

register(APPLICATION_ID, REST_API_KEY)

def parseMeetString(meetString):
	m, t, w, r, f = 0, 0, 0, 0, 0
	meetString = str.split(str(meetString))
	if len(meetString) > 3:
		for i in range(3, len(meetString)):
			meetString[2] = meetString[2] + ' ' + meetString[i]
	meetString = meetString[:3]
	if meetString[0].find("M"):
		m = 1
	if meetString[0].find("T"):
		t = 1
	if meetString[0].find("W"):
		w = 1
	if meetString[0].find("R"):
		r = 1
	if meetString[0].find("F"):
		f = 1
	time = meetString[1][:13]
	startTime, endTime = time.split('-')
	startTime += 'M'
	endTime += 'M'
	startTime = datetime.time(datetime.strptime(startTime, "%I:%M%p"))
	endTime = datetime.time(datetime.strptime(endTime, "%I:%M%p"))
	building = ''.join([i for i in meetString[2] if not i.isdigit()])
	roomNumber = filter(str.isdigit, meetString[2])

	return [m, t, w, r, f], startTime, endTime, building, roomNumber

with open('doc.json') as data_file:
	data = json.load(data_file)
data_to_upload = []
for course in range(len(data)):
	current = data[course]
	if current['Term'] == '20151' and current['Meets1'] != '' and 'RTBA' not in str(current['Meets1']):
		if current['DivisionCode'] == 'CC' or current['DivisionName'] == 'SCH OF ENGR & APP SCI: UGRAD' or current['DivisionCode'] == 'BC' or current['DivisionCode'] == 'GS':
				newClass = ParseObject()
				newClass.class_code = current['Course']
				newClass.instructor = current['Instructor1Name']
				newClass.name = current['CourseTitle']
				#call function that gets location, start, and end time
				newClass.days, newClass.startTime, newClass.endTime, newClass.building, newClass.roomNumber = parseMeetString(current['Meets1'])
				data_to_upload.append(newClass)

print "x"
batcher = ParseBatcher()
for x in range(0, len(data_to_upload), 50):
	batcher.batch_save(data_to_upload[x: x+50 if (x+50) < len(data_to_upload) else len(data_to_upload)])
