from django.urls import path
from . import views

app_name = 'bag'

urlpatterns = [
    path('add/', views.bag_add, name='bag_add'),
    path('remove/<int:variant_id>/', views.bag_remove, name='bag_remove'),
]