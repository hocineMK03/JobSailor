# Generated by Django 4.2.6 on 2023-11-15 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_remove_theuser_resume_theuser_worker_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theuser_company',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='theuser_company',
            name='websitelink',
        ),
        migrations.RemoveField(
            model_name='theuser_worker',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='theuser_worker',
            name='websitelink',
        ),
    ]
