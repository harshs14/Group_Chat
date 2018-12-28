from django.conf.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$', views.Register.as_view(), name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.Activate.as_view(), name='activate'),
    # re_path(r'^home/$', views.Home.as_view(), name='home'),
    re_path(r'^login/$', views.Login.as_view(), name='login'),
    re_path(r'^profile/(?P<user_id>[0-9]+)/$', views.UserProfile.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
