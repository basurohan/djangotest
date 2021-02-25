from django.contrib import admin

# Register your handlers here.
from classroom.models import Student, Classroom

admin.site.register(Student)
admin.site.register(Classroom)

