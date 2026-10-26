from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-task/', views.add_task, name='add_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),

]
