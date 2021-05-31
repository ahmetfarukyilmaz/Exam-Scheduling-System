# Generated by Django 3.2.3 on 2021-05-31 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_school_accesskey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='accessKey',
        ),
        migrations.AddField(
            model_name='school',
            name='adminAccessKey',
            field=models.CharField(blank=True, default='abc123123', max_length=100, null=True, verbose_name='adminAccesssKey'),
        ),
        migrations.AddField(
            model_name='school',
            name='teacherAccessKey',
            field=models.CharField(blank=True, default='abc123', max_length=100, null=True, verbose_name='teacherAccessKey'),
        ),
    ]