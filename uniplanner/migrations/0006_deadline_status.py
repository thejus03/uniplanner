# Generated by Django 4.2.5 on 2023-10-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniplanner', '0005_toask_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='deadline',
            name='status',
            field=models.CharField(default='undone', max_length=30),
        ),
    ]
