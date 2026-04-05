import pandas as pd
import matplotlib.pyplot as plt
import io


class CourseAnalyzer:
    """Класс для анализа данных о записях на курсы."""

    def __init__(self, enroll_source, courses_source, is_file_path=True):
        """
        Инициализация класса.
        is_file_path=True означает, что переданы пути к файлам.
        is_file_path=False используется для передачи бинарных данных (например, из API).
        """
        if is_file_path:
            self.enroll_df = pd.read_csv(enroll_source)
            self.courses_df = pd.read_csv(courses_source)
        else:
            self.enroll_df = pd.read_csv(io.BytesIO(enroll_source))
            self.courses_df = pd.read_csv(io.BytesIO(courses_source))

        self.merged_df = None
        self.top_courses_df = None

    def get_common_codes(self):
        """Пункт 9: Пересечение множеств кодов курсов."""
        enroll_codes = self.enroll_df['course_code'].unique()
        courses_codes = self.courses_df['course_code'].unique()
        return set(enroll_codes).intersection(set(courses_codes))

    def clean_courses(self):
        """Пункт 10: Сортировка и удаление дубликатов в справочнике."""
        self.courses_df = self.courses_df.drop_duplicates(subset=['course_code']).sort_values('course_code')

    def merge_data(self):
        """Пункт 11: Объединение таблиц по course_code."""
        self.merged_df = self.enroll_df.merge(self.courses_df, on='course_code', how='inner')

    def calculate_top_courses(self):
        """Пункт 12: Подсчет уникальных студентов."""
        if self.merged_df is None:
            self.merge_data()

        self.top_courses_df = (
            self.merged_df.groupby('title')['student_id']
            .nunique()
            .reset_index()
            .rename(columns={'student_id': 'student_count'})
            .sort_values(by='student_count', ascending=False)
        )
        return self.top_courses_df

    def save_top_courses_csv(self, filename='top_courses.csv'):
        """Сохранение результата в CSV."""
        if self.top_courses_df is not None:
            self.top_courses_df.to_csv(filename, index=False)
            print(f"Файл {filename} успешно сохранен.")

    def plot_top_courses(self, top_n=7, filename='top_7_courses.png'):
        """Пункт 13: Построение горизонтального bar-графика."""
        if self.top_courses_df is None:
            self.calculate_top_courses()

        top_n_df = self.top_courses_df.head(top_n)

        plt.figure(figsize=(10, 6))
        plt.barh(top_n_df['title'], top_n_df['student_count'], color='skyblue')
        plt.gca().invert_yaxis()
        plt.xlabel('Количество уникальных студентов')
        plt.ylabel('Название курса')
        plt.title(f'Топ-{top_n} курсов по количеству студентов')
        plt.tight_layout()

        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"График {filename} успешно сохранен.")

    def run_full_pipeline(self):
        """Запуск всего пайплайна обработки."""
        print(f"Общих кодов: {len(self.get_common_codes())}")
        self.clean_courses()
        self.merge_data()
        self.calculate_top_courses()
        self.save_top_courses_csv()
        self.plot_top_courses()


# --- Использование класса локально ---
if __name__ == "__main__":
    # Предполагается, что файлы лежат в той же директории
    analyzer = CourseAnalyzer('enroll.csv', 'courses.csv')
    analyzer.run_full_pipeline()





# FastAPI
from fastapi import FastAPI, UploadFile, File

# Импортируем наш класс (если он в файле analyzer.py, то: from analyzer import CourseAnalyzer)
# В рамках этого примера предполагаем, что класс доступен в той же области видимости.

app = FastAPI()


@app.post("/top-courses")
async def get_top_courses(
        enroll_file: UploadFile = File(...),
        courses_file: UploadFile = File(...)
):
    # Читаем содержимое файлов
    enroll_bytes = await enroll_file.read()
    courses_bytes = await courses_file.read()

    # Создаем экземпляр анализатора, указывая is_file_path=False
    analyzer = CourseAnalyzer(enroll_bytes, courses_bytes, is_file_path=False)

    # Выполняем необходимые шаги пайплайна
    analyzer.clean_courses()
    analyzer.merge_data()
    top_courses_df = analyzer.calculate_top_courses()

    # Возвращаем JSON
    return top_courses_df.to_dict(orient="records")