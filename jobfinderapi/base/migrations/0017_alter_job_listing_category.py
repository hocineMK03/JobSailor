# Generated by Django 4.2.6 on 2023-10-17 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_job_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.job_category'),
        ),
    ]