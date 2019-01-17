from django.urls import path
from . import views

#created paths for visualPDF app views
urlpatterns = [
    path('',views.form, name = 'form'),
    path('about/', views.about, name = 'about')
]
