# chat/routing.py
from django.conf.urls import url, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^testgroup/(?P<g_id>[0-9]+)/$', consumers.GroupMessageConsumer),
]
