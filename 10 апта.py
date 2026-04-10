import pandas as pd

enroll = pd.read_csv('enroll.csv')
courses = pd.read_csv('courses.csv')

courses_cleaned = courses.drop_duplicates(subset=['course_code']).sort_values('course_code')

merged_df = pd.merge(enroll, courses_cleaned, on='course_code')
result = merged_df.groupby('title')['student_id'].count().reset_index()

print("Сұрыпталған және тазартылған анықтамалық бойынша нәтиже: ")
print(result)