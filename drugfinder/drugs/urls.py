from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^send_image/$', views.SendImage.as_view()),
	url(r'^get_sampled_data/$', views.GetSampledData.as_view()),
]
