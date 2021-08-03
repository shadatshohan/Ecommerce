from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='shopHome'),
    path('product/<int:myid>',views.prodview,name='productview'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('checkout/', views.checkout,name='checkout'),
    path('search/', views.search,name='search'),
    path('tracker/', views.tracker,name='tracker'),
]