# Generated by Django 4.2.16 on 2024-09-18 16:58

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('linkedin_link', models.URLField(blank=True)),
                ('summary', models.TextField(blank=True)),
                ('skills', models.TextField(blank=True, help_text='Enter skills separated by commas or new lines.')),
                ('publications', models.TextField(blank=True, help_text='Enter publications separated by commas or new lines.')),
                ('projects', models.TextField(blank=True, help_text='Enter projects separated by commas or new lines.')),
                ('interests', models.TextField(blank=True, help_text='Enter interests separated by commas or new lines.')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education_level', models.CharField(max_length=100)),
                ('university', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('specialization', models.CharField(blank=True, max_length=255)),
                ('thesis', models.CharField(blank=True, max_length=255)),
                ('relevant_subjects', models.TextField(blank=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='core.userprofile')),
            ],
        ),
    ]
