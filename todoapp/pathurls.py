from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_todos, name="list_todos"),
    path("todo/<int:pk>", views.list_todo, name="list_todo"),
    path("create/", views.create_todo, name="create_todo"),
    path("update/<int:pk>", views.update_todo, name="update_todo"),
    path("delete/<int:pk>", views.delete_todo, name="delete_todo"),
]