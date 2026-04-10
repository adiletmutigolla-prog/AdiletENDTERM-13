import pandas as pd

enroll = pd.read_csv('enroll.csv')
courses = pd.read_csv('courses.csv')

merged_df = pd.merge(enroll, courses, on='course_code')
result = merged_df.groupby('title')['student_id'].count().reset_index()

print(result)

codes_enroll = enroll['course_code'].unique()
codes_courses = courses['course_code'].unique()
intersection = list(set(codes_enroll) & set(codes_courses))

print(intersection)