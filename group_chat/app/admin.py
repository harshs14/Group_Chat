from django.contrib import admin

from .models import Member, Group, Message

admin.site.register(Member)
admin.site.register(Group)
admin.site.register(Message)

