from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.consumers import GroupMessageConsumer
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator


application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
           URLRouter(
               [
                   url(r'^test_group/(?P<g_id>[0-9]+)/$', GroupMessageConsumer),
               ]
           )
        )
    )
})
