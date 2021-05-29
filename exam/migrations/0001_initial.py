# Generated by Django 3.2.3 on 2021-05-29 16:03

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('postalCode', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('studentSittingPlan', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(choices=[('1', '9'), ('2', '10'), ('3', '11'), ('4', '12')], default='1', max_length=20)),
                ('branch', models.CharField(choices=[('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D'), ('5', 'E'), ('6', 'F'), ('7', 'G'), ('8', 'H'), ('9', 'I')], default='1', max_length=20)),
                ('deskPlan', models.TextField()),
                ('floor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.OneToOneField(db_column='Teacher Address', on_delete=django.db.models.deletion.CASCADE, to='exam.address')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=100)),
                ('schoolNumber', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.OneToOneField(db_column='Student Address', on_delete=django.db.models.deletion.CASCADE, to='exam.address')),
                ('exams', models.ManyToManyField(to='exam.Exam')),
                ('schoolClass', models.ForeignKey(db_column='schoolClass-Student FK', on_delete=django.db.models.deletion.CASCADE, to='exam.schoolclass')),
            ],
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='representative',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exam.student'),
        ),
        migrations.CreateModel(
            name='SchoolAdministrator',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.OneToOneField(db_column='School Admin Address', on_delete=django.db.models.deletion.CASCADE, to='exam.address')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('address', models.OneToOneField(db_column='School Address', on_delete=django.db.models.deletion.CASCADE, to='exam.address')),
                ('schoolAdministrator', models.ForeignKey(db_column='School-SchoolAdministrator FK', on_delete=django.db.models.deletion.CASCADE, to='exam.schooladministrator')),
                ('schoolClass', models.ForeignKey(db_column='School-SchoolClass FK', on_delete=django.db.models.deletion.CASCADE, to='exam.schoolclass')),
                ('teacher', models.ForeignKey(db_column='School-Teacher FK', on_delete=django.db.models.deletion.CASCADE, to='exam.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('administrator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exam.schooladministrator')),
                ('exams', models.ManyToManyField(to='exam.Exam')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='classes',
            field=models.ManyToManyField(related_name='classes', to='exam.SchoolClass'),
        ),
        migrations.AddField(
            model_name='exam',
            name='examLocation',
            field=models.ManyToManyField(related_name='examLocation', to='exam.SchoolClass'),
        ),
        migrations.AddField(
            model_name='exam',
            name='observerTeacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='observer_teacher', to='exam.teacher'),
        ),
        migrations.AddField(
            model_name='exam',
            name='ownerTeacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner_teacher', to='exam.teacher'),
        ),
    ]
