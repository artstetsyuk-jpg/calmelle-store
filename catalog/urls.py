from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('lang/<str:lang_code>/', views.set_language, name='set_language'),
    path('piece/<slug:slug>/', views.product_detail, name='product_detail'),
]