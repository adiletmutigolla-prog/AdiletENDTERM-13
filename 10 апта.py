import pandas as pd

class CourseManager:
    def __init__(self, enroll_path, courses_path):
        self.enroll = pd.read_csv(enroll_path)
        self.courses = pd.read_csv(courses_path)

    def clean_courses(self):
        self.courses = self.courses.drop_duplicates(subset=['course_code']).sort_values('course_code')

    def get_student_counts(self):
        self.clean_courses()
        merged_df = pd.merge(self.enroll, self.courses, on='course_code')
        return merged_df.groupby('title')['student_id'].count().reset_index()

task10 = CourseManager('enroll.csv', 'courses.csv')
print(task10.get_student_counts())