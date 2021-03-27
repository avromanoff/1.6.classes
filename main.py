class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):  # выставление оценки лектору
        grade_list = list(range(11))
        if grade not in grade_list:
            return 'оценки должна быть в диапазоне 1...10'
        else:
            if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
                if course in lecturer.lecturer_grade:
                    lecturer.lecturer_grade[course] += [grade]
                else:
                    lecturer.lecturer_grade[course] = [grade]
        return

    def student_average_grade(self):  # вычисление средней оценки по всем предметам
        total_result = 0
        total_len = 0
        for grade in self.grades.values():
            total_result += sum(grade)
            total_len += len(grade)
        if total_len == 0:
            average_result = 'оценок нет'
        else:
            average_result = total_result / total_len
        return average_result

    def __str__(self):  # переназначение print
        courses_in_progress_string = ', '.join(self.courses_in_progress)
        finished_courses_string = ', '.join(self.finished_courses)
        return f'Имя: {self.name}\nФамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self.student_average_grade()}\n' \
               f'Курсы в процессе изучения: {courses_in_progress_string}\n' \
               f'Завершенные курсы: {finished_courses_string}\n '

    def __gt__(self, other):  # сравнение студентов
        if not isinstance(other, Student):
            return 'Сравниваются только студенты'
        if self.student_average_grade() > other.student_average_grade():
            return f'Успеваемость {self.name} лучше, чем {other.name}\n'
        else:
            return f'Успеваемость {self.name} хуже, чем {other.name}\n'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.lecturer_grade = {}

    def lecturer_avg_grade(self):  # средняя оценка лектора по оценкам студентов
        lecturer_total_result = 0
        lecturer_total_len = 0
        for grade in self.lecturer_grade.values():
            lecturer_total_result += sum(grade)
            lecturer_total_len += len(grade)
        if lecturer_total_len == 0:
            lecturer_average_result = 'оценок нет'
        else:
            lecturer_average_result = lecturer_total_result / lecturer_total_len
        return lecturer_average_result

    def __str__(self):  # переназначение print
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.lecturer_avg_grade()}\n'

    def __gt__(self, other):  # сравнение лекторов
        if not isinstance(other, Lecturer):
            return 'Сравниваются только лекторы'
        if self.lecturer_avg_grade() > other.lecturer_avg_grade():
            return f'{self.name} оценивают выше, чем {other.name}\n'
        else:
            return f'{self.name} оценивают ниже, чем {other.name}\n'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):  # выставление оценок студентам
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):  # переназначение print
        return f'Имя: {self.name}\nФамилия: {self.surname}\n'


# для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса
# (в качестве аргументов принимаем список студентов и название курса);

def average_grade_student_course(std_list, course):
    print(f'Средняя оценка студентов на курсе {course}:')
    student_counter = 0
    total_grade = 0
    for student in std_list:
        if course in student.courses_in_progress:
            if course not in student.grades.keys():
                return 'Оценок нет'
            student_counter += 1
            stud_avg_grd = sum(student.grades.get(course))/len(student.grades.get(course))
            total_grade += stud_avg_grd
    total_average = total_grade/student_counter
    return total_average

# для подсчета средней оценки за лекции всех лекторов в рамках конкретного курса
# (в качестве аргументов принимаем список лекторов и название курса).


def average_grade_lecturer_course(lect_list, course):
    print(f'Средняя оценка лекторов на курсе {course}:')
    lecturer_counter = 0
    total_grade = 0
    for lecturer in lect_list:
        if course in lecturer.courses_attached:
            if course not in lecturer.lecturer_grade.keys():
                return 'Оценок нет'
            lecturer_counter += 1
            lect_avg_grd = sum(lecturer.lecturer_grade.get(course)) / len(lecturer.lecturer_grade.get(course))
            total_grade += lect_avg_grd
    total_average = total_grade / lecturer_counter
    return total_average


# представители классов
best_student = Student('James', 'Bond', 'man')
best_student.courses_in_progress += ['Python']
best_student.finished_courses += ['Web']

studentessa = Student('Mary', 'Jane', 'female')
studentessa.courses_in_progress += ['Python']
studentessa.courses_in_progress += ['Web']

# список студентов -- можно ли его собирать программно???
students_list = [best_student, studentessa]

reviewer_1 = Reviewer('Some', 'Buddy')
reviewer_1.courses_attached += ['Python']
reviewer_1.courses_attached += ['Web']
reviewer_1.rate_hw(best_student, 'Python', 10)
reviewer_1.rate_hw(best_student, 'Python', 10)
reviewer_1.rate_hw(studentessa, 'Python', 8)
reviewer_1.rate_hw(studentessa, 'Web', 8)

reviewer_2 = Reviewer('Silly', 'Billy')
reviewer_2.courses_attached += ['Python']
reviewer_2.rate_hw(best_student, 'Python', 6)
reviewer_2.rate_hw(studentessa, 'Python', 5)

lecturer_1 = Lecturer('Bill', "G")
lecturer_1.courses_attached += ['Python']

lecturer_2 = Lecturer('Richard', "S")
lecturer_2.courses_attached += ['Python']
lecturer_2.courses_attached += ['Web']

lecturers_list = [lecturer_1, lecturer_2]

best_student.rate_lecturer(lecturer_1, 'Python', 1)
best_student.rate_lecturer(lecturer_2, 'Python', 2)
studentessa.rate_lecturer(lecturer_1, 'Python', 1)
studentessa.rate_lecturer(lecturer_2, 'Python', 10)

print(best_student)
print(studentessa)
print(best_student > studentessa)
print(reviewer_1)
print(reviewer_2)
print(lecturer_1)
print(lecturer_2)
print(lecturer_1 > lecturer_2)
print(average_grade_student_course(students_list, 'Web'))
print(average_grade_student_course(students_list, 'Python'))
print(average_grade_lecturer_course(lecturers_list, 'Web'))
print(average_grade_lecturer_course(lecturers_list, 'Python'))
