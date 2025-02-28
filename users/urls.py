from django.urls import path
from users.views import sing_up, sing_in, sing_out, activate_user, admin_dashboard,assign_role,create_group, group_list

urlpatterns = [
    path('sing-up/', sing_up, name='sing-up'),
    path('sing-in/', sing_in, name='sing-in'),
    path('sing-out/', sing_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list', group_list, name='group-list')

]
