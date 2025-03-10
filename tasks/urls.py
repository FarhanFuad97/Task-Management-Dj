from django.urls import path # type: ignore
from tasks.views import manager_dashboard, employee_dashboard,create_task,view_task, task_deatils,dashboard, Greetings,HiGreetings, CreateTask

urlpatterns = [
    # path('manager-dashboard/', manager_dashboard , name = "manager-dashboard"),
    path('manager-dashboard/', manager_dashboard.as_view(), name='manager-dashboard'),
    path('user-dashboard/', employee_dashboard, name='user-dashboard'),
    # path('create-task/', create_task, name = 'create-task'),
    path('create-task/', CreateTask.as_view(), name = 'create-task'),
    # path('view_task/', view_task),
    
    path('task/<int:task_id>/details/', task_deatils, name='task-details'),
    path('dashboard', dashboard, name='dashboard'),
    path('greetings/', HiGreetings.as_view(),  name='greetings')
    
]
