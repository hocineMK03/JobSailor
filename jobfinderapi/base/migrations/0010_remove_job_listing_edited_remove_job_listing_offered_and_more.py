# Generated by Django 4.2.6 on 2023-10-16 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_job_listing_offered_job_pending_job_accepted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_listing',
            name='edited',
        ),
        migrations.RemoveField(
            model_name='job_listing',
            name='offered',
        ),
        migrations.RemoveField(
            model_name='job_listing',
            name='posted_at',
        ),
    ]
