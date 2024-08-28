from django.urls import path
from .views import PostList

urlpatterns = [
    path('api/posts/', PostList.as_view()),
]