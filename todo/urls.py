from django.urls import path, include
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskLoginView, RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', TaskLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path("", TaskListView.as_view(), name="task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name='task_update'),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name='task_delete'),
]