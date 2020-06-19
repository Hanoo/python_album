from django.urls import path

from user import views

urlpatterns = [
    path('new_hello/', views.new_hello),
    path('gallery/', views.gallery),
    path('get_album_list/', views.get_album_list),
    path('get_file_list', views.get_file_list),

]
