from django.conf.urls import url
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
	url(r'^login/', admin.site.urls),
	url(r'^signup/$', views.SignUp.as_view()),
	url(r'^signin/$', views.SignIn.as_view()),
	url(r'^obtain_token/$', obtain_jwt_token),
	url(r'^refresh_token/$', refresh_jwt_token),
	url(r'^change_password/$', views.ChangePassword.as_view()),
	url(r'^change_profile/$', views.ChangeProfile.as_view()),
	url(r'^get_name/$', views.GetName.as_view()),
]

