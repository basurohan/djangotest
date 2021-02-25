from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, permissions, authentication

from classroom.api.serializers import StudentSerializer, ClassroomSerializer
from classroom.models import Student, Classroom


class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassroomNumberAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, *args, **kwargs):
        capacity = self.kwargs.get('capacity', None)
        classrooms = Classroom.objects.filter(student_capacity__gte=capacity)
        serializer = ClassroomSerializer(classrooms, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
