from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.consumers import GroupMessageConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
           url(r'^test_group/(?P<g_id>[0-9]+)/$', GroupMessageConsumer),
        ])
    ),

})
