from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^get_history/$', views.GetHistory.as_view()),
	url(r'^bookmark/$', views.Bookmark.as_view()),
]
