# chat/routing.py
from django.conf.urls import url, re_path

from . import consumers

websocket_urlpatterns = [
    url(r'^testgroup/(?P<g_id>[0-9]+)/$', consumers.TestGroupMessageConsumer),
    url(r'^group/(?P<g_id>[0-9]+)/$', consumers.GroupMessageConsumer),
]

