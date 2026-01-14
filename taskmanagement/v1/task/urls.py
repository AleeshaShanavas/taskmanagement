from django.urls import path
from v1.task.view import views
from v1.task.view import admin_views

urlpatterns = [
    # tasks
    path('', views.get_user_tasks, name='user-tasks'),
    path('<int:id>/', views.update_task_status, name='update-task-status'),
    path('<int:id>/report/', views.get_task_report, name='task-report'),

    # Admin-specific views
    path('admin/', admin_views.admin_dashboard, name='admin_dashboard'),
    path(
        'admin/task/<int:task_id>/report/', admin_views.view_task_report, 
        name='view_task_report'),
    path('admin/assign-task/', admin_views.assign_task, name='assign_task'),
    path(
        'admin/assign-user-to-admin/<int:user_id>/', 
        admin_views.assign_user_to_admin, name='assign_user_to_admin'),
    path('admin/create-user/', admin_views.create_user, name='create_user'),
    path(
        'admin/update-user/<int:user_id>/', admin_views.update_user, 
        name='update_user'),
    path(
        'admin/delete-user/<int:user_id>/', admin_views.delete_user, 
        name='delete_user'),
]