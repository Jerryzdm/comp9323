import csv
from models import *
csvPath = 'course.csv'
with open(csvPath, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)
    for row in spamreader:
        new_course = Course()
        new_course.courseCode = row[1]
        new_course.courseName = row[3]
        new_course.courseUrl = row[4]
        new_course.repeateCourse = row[5]
        new_course.courseUOC = row[2]
        db.session.add(new_course)
    db.session.commit()
        #print(', '.join(row))