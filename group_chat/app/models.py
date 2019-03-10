from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class User(AbstractUser):

    name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
    avatar = models.ImageField(upload_to='member_pic', default='profile.png')

    def __str__(self):
        return self.username


class Group(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='group_pic', default='profile.png', null=True)
    members = models.ManyToManyField(User, related_name='%(class)s_member_of_group', null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_admin_of_group', null=True)

    def __str__(self):
        return "%s has created group: %s" % (self.admin, self.name)


class GroupMessage(models.Model):

    message = models.CharField(max_length=100, null=True)
    messaged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_message = models.FileField(upload_to='group_file_mesages', null=True, blank=True)
    time = models.DateTimeField(default=timezone.now, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Otp(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
