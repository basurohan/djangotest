import pytest
from mixer.backend.django import mixer
from hypothesis import given, strategies as st

from classroom.models import Student, Classroom


@pytest.mark.django_db
class TestStudentModel:

    def test_create_student(self):
        student = mixer.blend(Student, first_name='Tom')
        assert student.first_name == 'Tom'

    def test_student_str(self):
        student = mixer.blend(Student, first_name='Tom')
        assert str(student) == 'Tom'

    @given(st.floats(min_value=0, max_value=40))
    def test_grade_fail(self, fail_score):
        student = mixer.blend(Student, average_score=fail_score)
        student_result = Student.objects.last()
        assert student_result.get_grade() == 'Fail'

    @given(st.floats(min_value=40, max_value=70))
    def test_grade_pass(self, pass_score):
        student = mixer.blend(Student, average_score=pass_score)
        student_result = Student.objects.last()
        assert student_result.get_grade() == 'Pass'

    @given(st.floats(min_value=70, max_value=100))
    def test_grade_excellent(self, excellent_score):
        student = mixer.blend(Student, average_score=excellent_score)
        student_result = Student.objects.last()
        assert student_result.get_grade() == 'Excellent'

    @given(st.floats(min_value=101))
    def test_grade_error(self, error_score):
        student = mixer.blend(Student, average_score=error_score)
        student_result = Student.objects.last()
        assert student_result.get_grade() == 'Error'

    def test_slugify_username(self):
        student = mixer.blend(Student, first_name='Tom')
        student_result = Student.objects.last()
        assert student_result.first_name.lower() == student_result.username


@pytest.mark.django_db
class TestClassroomModel:

    def test_classroom_str(self):
        classroom = mixer.blend(Classroom, name='Engineering')
        assert str(classroom) == 'Engineering'
