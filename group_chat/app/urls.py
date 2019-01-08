from django.urls import re_path, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^$', views.Register.as_view(), name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.Activate.as_view(), name='activate'),
    # re_path(r'^home/$', views.Home.as_view(), name='home'),
    re_path(r'^login/$', views.Login.as_view(), name='login'),
    re_path(r'^profile/(?P<user_id>[0-9]+)/$', views.UserProfile.as_view(), name='user_profile'),
    re_path(r'^createprofile/$', views.CreateUserProfile.as_view(), name='create_profile'),
    re_path(r'^creategroup/$', views.CreateGroup.as_view(), name='create_group'),
    re_path(r'groupprofile/(?P<id>[0-9]+)/$', views.GroupProfile.as_view(), name='group_profile'),
    re_path(r'logout/$',views.Logout.as_view(), name='logout'),
    # path('addmembers/<int:pk>/', views.AddMember.as_view(), name='add_member'),
    re_path(r'contactlist/$', views.ContactList.as_view(), name='contact_list')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
