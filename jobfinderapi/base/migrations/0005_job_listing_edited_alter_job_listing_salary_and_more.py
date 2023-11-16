# Generated by Django 4.1.7 on 2023-10-09 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_job_listing_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_listing',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='job_listing',
            name='salary',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Theuser_messages',
            fields=[
                ('message_identifier', models.TextField(primary_key=True, serialize=False)),
                ('message_body', models.TextField()),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('message_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='base.theuser')),
                ('message_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='base.theuser')),
            ],
        ),
    ]
