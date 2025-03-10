from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.views.generic import CreateView,FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
# Create your views here.

#Test for users.........
def is_admin(user):
   return user.groups.filter(name='Admin').exists()



class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False  # Set the user as inactive initially for email confirmation
        user.save()

        # Send confirmation email logic should go here (e.g. send_mail)
        messages.success(self.request, 'A confirmation email has been sent. Please check your email.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Handle invalid form case if necessary
        return self.render_to_response(self.get_context_data(form=form))


# def sing_up(request):
#     form = CustomRegistrationForm()
#     if request.method == 'POST':
#        form = CustomRegistrationForm(request.POST)
#        if form.is_valid():
#           user = form.save(commit=False)
#           user.set_password(form.cleaned_data.get('password'))
#           user.is_active = False
#           user.save()
#           messages.success(request, 'A Confirmation mail sent. Please Check your email')
#           return redirect('sing-in')
          
             
#     return render(request, 'registration/register.html', {"form": form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')  # Redirect to home on successful login

    def form_valid(self, form):
        # If the form is valid, login the user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

# def sing_in(request):
#    form = LoginForm()
#    if request.method == 'POST':
#       form = LoginForm(data=request.POST)
#       if form.is_valid():
#           user = form.get_user()
#           login(request,user)
#           return redirect('home')
#    return render(request, 'registration/login.html', {'form': form})


class SignOutView(LogoutView):
    next_page = reverse_lazy('sign-in')

# @login_required
# def sing_out(request):
#    if request.method == 'POST':
#       logout(request)
#       return redirect('sing-in')


   
def activate_user(request, user_id, token):
   try:
      user = User.objects.get(id=user_id)
      if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('sing-in')
      else:
         return HttpResponse('Invaild Id or token')
   
   except User.DoesNotExist:
    return HttpResponse('User not found')

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
   users = User.objects.prefetch_related(
          Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
   ).all()

   for user in users:
      if user.all_groups:
         user.group_name= user.all_groups[0].name
      else:
         user.group_name = 'No Group Assigned'
   return render(request, 'admin/dashboard.html', {"users":users})


class AssignRoleView(FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignRoleForm

    def get_success_url(self):
        
        return reverse_lazy('admin-dashboard')

    def form_valid(self, form):
      
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        role = form.cleaned_data.get('role')

        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request, f"User {user.username} has been assigned to the {role.name} role")

        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @user_passes_test(is_admin, login_url='no-permission')
# def assign_role(request, user_id):
#    user = User.objects.get(id=user_id)
#    form = AssignRoleForm()

#    if request.method == 'POST':
#       form = AssignRoleForm(request.POST)
#       if form.is_valid():
#          role = form.cleaned_data.get('role')
#          user.groups.clear() # Remove old roles
#          user.groups.add(role)
#          messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
#          return redirect('admin-dashboard')
      
#    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
   form = CreateGroupForm()
   if request.method == 'POST':
      form = CreateGroupForm(request.POST)

      if form.is_valid():
         group = form.save()
         messages.success(request, f'Group {group.name} has been created successfully')
         return redirect('create-group')
      
   return render(request, 'admin/create_group.html', {'form':form})
@user_passes_test(is_admin, login_url='no-permission')   
def group_list(request):
   groups = Group.objects.prefetch_related('permissions').all()
   return render(request, 'admin/group_list.html', {'groups':groups})
   

    
