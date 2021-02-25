import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def validate_negative(value):
    if value < 0:
        raise ValidationError('Value must be positive')


class Student(models.Model):
    id = models.CharField(primary_key=True, editable=False, unique=True, max_length=36)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    admission_number = models.IntegerField(unique=True)
    username = models.SlugField(blank=True, null=True)
    is_qualified = models.BooleanField(default=False)
    average_score = models.FloatField(blank=True, null=True, validators=[validate_negative])

    def __str__(self):
        return self.first_name

    def get_grade(self):
        if 0 <= self.average_score < 40:
            return 'Fail'
        elif 40 <= self.average_score < 70:
            return 'Pass'
        elif 70 <= self.average_score <= 100:
            return 'Excellent'
        else:
            return 'Error'

    def save(self, *args, **kwargs):
        self.id = str(uuid.uuid4().hex) if self.id is None else self.id
        self.username = slugify(self.first_name)
        super(Student, self).save(*args, **kwargs)


class Classroom(models.Model):
    name = models.CharField(max_length=120)
    student_capacity = models.IntegerField()
    students = models.ManyToManyField('classroom.Student')

    def __str__(self):
        return self.name
