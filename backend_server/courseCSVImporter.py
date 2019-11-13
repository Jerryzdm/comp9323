import csv
from models import *
csvPath = 'course_info.csv'
def courseImporter():
    with open(csvPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            new_course = Course()
            new_course.courseCode = row[1]
            new_course.courseName = row[2]
            new_course.courseUrl = row[4]
            new_course.courseUOC = row[3]
            new_course.courseOverview = row[5]
            new_course.courseFaculty = row[6]
            new_course.courseSchool = row[7]
            new_course.courseStudyLevel = row[8]
            new_course.courseTerms = row[9]
            new_course.courseCampus = row[10]
            db.session.add(new_course)
        db.session.commit()
        # print(', '.join(row))