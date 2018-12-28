from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone


class Member(models.Model):

    GENDER_SET = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    user_obj = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100, blank=True,null=True)
    # email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
    date_of_birth = models.DateField(max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to='member_pic', default='profile.png')
    gender = models.CharField(max_length=10, choices=GENDER_SET, default='None')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_Member(sender, instance, created, **kwargs):
        if created:
            Member.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_Member(sender, instance, **kwargs):
        instance.member.save()


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
    file_message = models.FileField(upload_to ='shared_files', null=True, blank=True)
    time = models.DateTimeField(default=timezone.now, null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)