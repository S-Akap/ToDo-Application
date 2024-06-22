from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup-done/', views.SignUpDoneView.as_view(), name='signup_done'),

    path('home/', views.HomeView.as_view(), name='home'),

    path('account/<int:pk>/', views.AccountView.as_view(), name='account'),
    path('account/<int:pk>/update', views.AccountUpdateView.as_view(), name='account_update'),
    path('account/<int:pk>/password_update', views.PasswordUpdateView.as_view(), name='password_update'),
    path('account/<int:pk>/delete', views.AccountDeleteView.as_view(), name='account_delete'),

    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('classes/create/', views.ClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/update/', views.ClassUpdateView.as_view(), name='class_update'),
    path('classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),

    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/create_with_class/', views.TaskCreateWithClassView.as_view(), name='task_create_with_class'),
]