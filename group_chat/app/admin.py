from django.contrib import admin

from .models import Group, Message, User

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Message)

