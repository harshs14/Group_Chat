
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone


class Member(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
    avatar = models.ImageField(upload_to='member_pic', default='profile.png')

    def __str__(self):
        return self.user.username


class Group(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='group_pic', default='profile.png')
    members = models.ManyToManyField(Member)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Message(models.Model):

    message = models.CharField(max_length=100, null=True)
    messaged_by = models.OneToOneField(Member, on_delete=models.CASCADE)
    file_message = models.FileField(upload_to='shared_files', null=True, blank=True)
    time = models.DateTimeField(default=timezone.now, null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)