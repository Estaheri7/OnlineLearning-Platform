# Generated by Django 4.2 on 2024-08-08 07:51

import courses.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_remove_course_price_alter_assignment_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to=courses.models.get_upload_to_assignments),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
