from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls


urlpatterns = [

    re_path(r'^$', views.Register.as_view(), name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.Activate.as_view(), name='activate'),
    # re_path(r'^home/$', views.Home.as_view(), name='home'),
    re_path(r'^login/$', views.Login.as_view(), name='login'),
    re_path(r'^profile/(?P<id>[0-9]+)/$', views.UserProfile.as_view(), name='user_profile'),
    # re_path(r'^createprofile/$', views.CreateUserProfile.as_view(), name='create_profile'),
    re_path(r'^creategroup/$', views.CreateGroup.as_view(), name='create_group'),
    re_path(r'^groupprofile/(?P<id>[0-9]+)/$', views.GroupProfile.as_view(), name='group_profile'),
    re_path(r'^logout/$', views.Logout.as_view(), name='logout'),
    # re_path(r'^addmembers/(?P<id>[0-9]+)/', views.AddMember.as_view(), name='add_member'),
    # re_path(r'^contactlist/$', views.ContactList.as_view(), name='contact_list'),
    re_path(r'^home/(?P<g_id>[0-9]+)/$', views.Message.as_view(), name='message'),
    re_path(r'^home/(?P<g_id>[0-9]+)/(?P<id>[0-9]+)/$', views.Message.as_view(), name='message_detail'),
    re_path(r'^docs/', include_docs_urls(title='My API title'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
