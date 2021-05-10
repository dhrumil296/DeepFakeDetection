from django.conf.urls import url
from django.urls import path
from deepfake.views import predictVideo, predictImage
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path('', views.main, name="index"),
    path('predict-image/', views.predictImage,name="predictImage"),
    path('predict-video/',views.predictVideo,name="predictVideo"),
    url('predictImg',views.predictImage,name="predictImage"),
    url('predictVideo',views.predictVideo,name="predictVideo")     
]