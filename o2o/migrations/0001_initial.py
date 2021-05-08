# Generated by Django 3.2.2 on 2021-05-07 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('entry_date', models.DateField(auto_now_add=True)),
                ('sex', models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cafeteria',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='o2o.place')),
                ('administrator', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='acafeteria', to='o2o.employee')),
                ('cleaner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='ccafeteria', to='o2o.employee')),
            ],
            options={
                'verbose_name': 'cafeteria',
                'verbose_name_plural': 'cafeterias',
            },
        ),
    ]