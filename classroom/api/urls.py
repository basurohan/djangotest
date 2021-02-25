from django.urls import path

from classroom.api.views import StudentListCreateView, StudentDetailView, ClassroomNumberAPIView

urlpatterns = [
    path('students', StudentListCreateView.as_view(), name='student_list_create_api'),
    path('student/<str:pk>', StudentDetailView.as_view(), name='student_detail_api'),
    path('class/<int:capacity>', ClassroomNumberAPIView.as_view(), name='class_qs_api'),
]
