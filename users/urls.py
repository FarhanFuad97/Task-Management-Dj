from django.urls import path
from users.views import  activate_user, admin_dashboard,create_group, group_list, SignUpView,CustomLoginView, SignOutView, AssignRoleView

urlpatterns = [
    # path('sing-up/', sing_up, name='sing-up'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # path('sing-in/', sing_in, name='sing-in'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('sing-out/', sing_out, name='logout'),
     path('sign-out/', SignOutView.as_view(), name='sign-out'),
     
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    # path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('assign-role/<int:user_id>/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list', group_list, name='group-list')

]
