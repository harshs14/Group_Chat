from django.contrib import admin

from .models import Group, GroupMessage, User

admin.site.register(User)
admin.site.register(Group)
admin.site.register(GroupMessage)

