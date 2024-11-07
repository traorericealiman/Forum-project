# forum/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/add_reply/', views.add_reply, name='add_reply'),  # URL pour ajouter une réponse
    path('ajouter/', views.add_post, name='add_post'),
]
