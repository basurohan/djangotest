# Generated by Django 3.1.7 on 2021-02-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_auto_20210222_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(editable=False, max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
