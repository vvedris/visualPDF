from django.urls import path
from . import views

urlpatterns = [
    path('',views.form, name = 'form'),
    path('form_plot/', views.form_plot, name = 'form_plot'),
    path('form_detail/',views.form_detail, name = 'form_detail')
]
