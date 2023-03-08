# Generated by Django 3.2.5 on 2023-03-08 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('column_separator', models.CharField(choices=[(',', 'Comma (,)'), ('.', 'Dot (.)')], default='Comma (,)', max_length=5)),
                ('string_character', models.CharField(blank=True, choices=[('"', 'Double-quote (")'), ("'", "Single-quote (')")], max_length=6)),
                ('modified', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, upload_to='')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fake_csv_app.schema')),
            ],
            options={
                'get_latest_by': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=128)),
                ('column_type', models.CharField(choices=[('full_name', 'Full name'), ('job', 'Job'), ('email', 'Email'), ('domain_name', 'Domain name'), ('phone_number', 'Phone number'), ('company_name', 'Company Name'), ('integer', 'Integer'), ('text', 'Text'), ('address', 'Address'), ('date', 'Date')], max_length=32)),
                ('from_range', models.IntegerField(blank=True, null=True)),
                ('to_range', models.IntegerField(blank=True, null=True)),
                ('order', models.IntegerField(default=1)),
                ('schema', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='fake_csv_app.schema')),
            ],
        ),
    ]