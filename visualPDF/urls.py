from django.urls import path
from . import views

#created paths for visualPDF app views
urlpatterns = [
    path('',views.form, name = 'form'),
    path('form_plot/', views.form_plot, name = 'form_plot'),
    path('form_detail/',views.form_detail, name = 'form_detail'),
    path('form_picture/',views.form_picture, name = 'form_picture')
]
