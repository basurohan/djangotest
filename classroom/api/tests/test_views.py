import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token

from classroom.models import Student, Classroom


def create_test_user():
    get_user_model().objects.create_user(
        username='test_user',
        password='abcd'
    )


@pytest.mark.django_db
class TestStudentAPIViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.student = mixer.blend(Student, first_name='Geoffrey')
        self.student_result = Student.objects.last()
        create_test_user()
        # self.test_user = get_user_model().objects.create_user(
        #     username='test_user',
        #     password='abcd'
        # )
        # self.token = Token.objects.create(user=self.test_user)
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = dict(username='test_user', password='abcd')
        self.token = self.client.post(reverse('token-url'), data=data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.data["token"]}')

    def test_student_create_works(self):
        data = dict(
            first_name='Wangari',
            last_name='Maathai',
            admission_number=22234,
            is_qualified=True,
            average_score=74
        )
        response = self.client.post(reverse('student_list_create_api'), data=data)

        assert response.status_code == 201
        assert response.json() is not None

    def test_student_list_works(self):
        response = self.client.get(reverse('student_list_create_api'))

        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json()) == 1
        assert response.json()[0]['first_name'] == 'Geoffrey'

    def test_student_retrieve_works(self):
        response = self.client.get(reverse('student_detail_api', kwargs={'pk': self.student_result.id}))

        assert response.status_code == 200
        assert response.json() is not None
        assert response.json()['first_name'] == 'Geoffrey'

    def test_put_update_works(self):
        self.student_result.average_score = 55
        data = dict(
            first_name=self.student_result.first_name,
            last_name=self.student_result.last_name,
            admission_number=self.student_result.admission_number,
            is_qualified=self.student_result.is_qualified,
            average_score=self.student_result.average_score
        )
        response = self.client.put(
            reverse('student_detail_api', kwargs={'pk': self.student_result.id}),
            data=data
        )

        assert response.status_code == 200
        assert response.json()['average_score'] == 55

    def test_student_delete_works(self):
        response = self.client.delete(reverse('student_detail_api', kwargs={'pk': self.student_result.id}))

        assert response.status_code == 204


@pytest.mark.django_db
class TestClassroomAPIViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.classroom = mixer.blend(Classroom, student_capacity=20)
        create_test_user()
        # self.test_user = get_user_model().objects.create_user(
        #     username='test_user',
        #     password='abcd'
        # )
        # self.token = Token.objects.create(user=self.test_user)
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = dict(username='test_user', password='abcd')
        self.token = self.client.post(reverse('token-url'), data=data)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.data["token"]}')

    def test_get_classroom_by_capacity_returns_classes(self):
        response = self.client.get(reverse('class_qs_api', kwargs={'capacity': 15}))

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 1

    def test_get_classroom_by_capacity_returns_no_classes(self):
        response = self.client.get(reverse('class_qs_api', kwargs={'capacity': 25}))

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 0
