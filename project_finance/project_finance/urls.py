
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from app_finance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_finance.urls')),
    # path('', views.IndexView.as_view(), name="index"),
    # path('plot/', views.PlotView.as_view(), name="plot"),
]
