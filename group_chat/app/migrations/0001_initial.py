# Generated by Django 2.1.4 on 2019-01-10 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('avatar', models.ImageField(default='profile.png', upload_to='group_pic')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_admin_of_group', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='group_member_of_group', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128)),
                ('avatar', models.ImageField(default='profile.png', upload_to='member_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100, null=True)),
                ('file_message', models.FileField(blank=True, null=True, upload_to='shared_files')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Group')),
                ('messaged_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Member')),
            ],
        ),
    ]
