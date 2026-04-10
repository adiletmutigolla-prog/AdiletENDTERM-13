import pandas as pd

class CourseIntersection:
    def __init__(self, enroll_path, courses_path):
        self.enroll = pd.read_csv(enroll_path)
        self.courses = pd.read_csv(courses_path)

    def get_intersection(self):
        codes_enroll = set(self.enroll['course_code'].unique())
        codes_courses = set(self.courses['course_code'].unique())
        return list(codes_enroll & codes_courses)

task9 = CourseIntersection('enroll.csv', 'courses.csv')
print(task9.get_intersection())