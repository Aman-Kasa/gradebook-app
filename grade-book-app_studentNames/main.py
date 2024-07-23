#!/usr/bin/python3


class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.GPA = 0.0

    def calculate_GPA(self):
        if not self.courses_registered:
            self.GPA = 0.0
        else:
            total_points = sum(course['grade'] * course['credits'] for course in self.courses_registered)
            total_credits = sum(course['credits'] for course in self.courses_registered)
            self.GPA = total_points / total_credits

    def register_for_course(self, course, grade):
        self.courses_registered.append({'course': course, 'grade': grade, 'credits': course.credits})
        self.calculate_GPA()


class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits


class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def add_student(self, student):
        self.student_list.append(student)

    def add_course(self, course):
        self.course_list.append(course)

    def register_student_for_course(self, student, course, grade):
        student.register_for_course(course, grade)

    def calculate_GPA(self):
        for student in self.student_list:
            student.calculate_GPA()

    def calculate_ranking(self):
        sorted_students = sorted(self.student_list, key=lambda s: s.GPA, reverse=True)
        return [(i + 1, student.names, student.GPA) for i, student in enumerate(sorted_students)]

    def search_by_grade(self, min_grade, max_grade):
        return [student for student in self.student_list if any(min_grade <= course['grade'] <= max_grade for course in student.courses_registered)]

    def generate_transcript(self, student):
        transcript = "Transcript for {}\n".format(student.names)
        for course in student.courses_registered:
            transcript += "{} - Grade: {} - Credits: {}\n".format(course['course'].name, course['grade'], course['credits'])
        transcript += "GPA: {}\n".format(student.GPA)
        return transcript


def main():
    gradebook = GradeBook()

    while True:
        print("\nChoose an action:")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate Ranking")
        print("5. Search by Grade")
        print("6. Generate Transcript")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter student's email: ")
            names = input("Enter student's names: ")
            student = Student(email, names)
            gradebook.add_student(student)
            print("Student added successfully.")

        elif choice == '2':
            name = input("Enter course name: ")
            trimester = input("Enter trimester: ")
            credits = int(input("Enter number of credits: "))
            course = Course(name, trimester, credits)
            gradebook.add_course(course)
            print("Course added successfully.")

        elif choice == '3':
            email = input("Enter student's email: ")
            student = next((s for s in gradebook.student_list if s.email == email), None)
            if student is None:
                print("Student not found.")
                continue
            course_name = input("Enter course name: ")
            course = next((c for c in gradebook.course_list if c.name == course_name), None)
            if course is None:
                print("Course not found.")
                continue
            grade = float(input("Enter grade: "))
            gradebook.register_student_for_course(student, course, grade)
            print("Student registered for course successfully.")

        elif choice == '4':
            gradebook.calculate_GPA()
            rankings = gradebook.calculate_ranking()
            for rank in rankings:
                print("Rank {}: {}, GPA: {}".format(rank[0], rank[1], rank[2]))

        elif choice == '5':
            min_grade = float(input("Enter minimum grade: "))
            max_grade = float(input("Enter maximum grade: "))
            students = gradebook.search_by_grade(min_grade, max_grade)
            for student in students:
                print(student.names)

        elif choice == '6':
            email = input("Enter student's email: ")
            student = next((s for s in gradebook.student_list if s.email == email), None)
            if student:
                transcript = gradebook.generate_transcript(student)
                print(transcript)
            else:
                print("Student not found.")

        elif choice == '7':
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
