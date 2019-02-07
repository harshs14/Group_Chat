from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from django.conf.urls import url,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'groupprofile', GroupProfile, basename='group_profile')

urlpatterns = [
    re_path(r'api/',include(router.urls)),
    re_path(r'^$', views.Register.as_view(), name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.Activate.as_view(), name='activate'),
    # re_path(r'^home/$', views.Home.as_view(), name='home'),
    re_path(r'^login/$', views.Login.as_view(), name='login'),
    re_path(r'^profile/(?P<id>[0-9]+)/$', views.UserProfile.as_view(), name='user_profile'),
    url(r'^new_group/$', views.CreateGroups.as_view(), name='create_group'),
    # re_path(r'^groupprofile/(?P<id>[0-9]+)/$', views.GroupProfile.as_view(), name='group_profile'),
    re_path(r'^logout/$', views.Logout.as_view(), name='logout'),
    # re_path(r'^addmembers/(?P<g_id>[0-9]+)/', views.AddMember.as_view(), name='add_member'),
    re_path(r'^contactlist/$', views.ContactList.as_view(), name='contact_list'),
    re_path(r'^group/(?P<g_id>[0-9]+)/$', views.Message.as_view(), name='message'),
    re_path(r'^group/(?P<g_id>[0-9]+)/(?P<id>[0-9]+)/$', views.Message.as_view(), name='message_detail'),
    url(r'^testgroup/(?P<g_id>[0-9]+)/$', views.TestMessage.as_view(), name='test_message'),
    re_path(r'^testgroup/(?P<g_id>[0-9]+)/(?P<id>[0-9]+)/$', views.TestMessage.as_view(), name='test_message_detail'),
    re_path(r'^group/$', views.GroupList.as_view(), name='group'),
                  url(r'^docs/', include_docs_urls(title='Your API',
                                                   authentication_classes=[],
                                                   permission_classes=[])),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
