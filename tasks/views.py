from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import  Task, TaskDetail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin



# variables for list of decorators


#Class Based View Re-use example
class Greetings(View):
    greeting = 'Hello Everyone'

    def get(self,request):
        return HttpResponse(self.greeting)
class HiGreetings(Greetings):
    greeting = 'Hi Everyone'

# Create your views here.
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Manager').exists()



@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get('type', 'all')

    

    
    counts = Task.objects.aggregate(
        total = Count('id'),
        completed = Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status = 'IN_PROGRESS')),
        pending=Count('id', filter=Q(status = 'PENDING')),


        )
    
    # Retriving task data

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status= 'COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status= 'IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status= 'PENDING')
    elif type == 'all':
        tasks = base_query.all()


    context = {
        "tasks": tasks,
        "counts": counts,
        "role": 'manager'
    }
    return render(request, "dashboard/manager-dashboard.html", context)
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm() #For Get
    task_detail_form = TaskDetailModelForm()


    if request.method == "POST":
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        
        if task_form.is_valid() and task_detail_form.is_valid():


            """ For Model Form Data """
            task =task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

   
            messages.success(request, "Task Created Successfully")
            return redirect('create-task') 
        
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


# variable for list of decorators
create_decorators = [login_required,permission_required("tasks.add_task", login_url='no-permission')]
  


class CreateTask(LoginRequiredMixin,PermissionRequiredMixin, ContextMixin,View):
    """ For creating task"""

    permission_required = 'tasks.add_task'
    login_url = 'sing-in'
    template_name = 'task_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context
        

    def get(self, request, *agrs, **kwargs):
        
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *agrs, **kwargs):
        if request.method == "POST":
         task_form = TaskModelForm(request.POST) 
         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        
        if task_form.is_valid() and task_detail_form.is_valid():


            """ For Model Form Data """
            task =task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

   
            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)


@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    projects = Project.objects.annotate(
        num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def task_deatils(request, task_id):
    
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)
    return render(request, 'task_details.html', {"task": task, "status_choices": status_choices})


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')





            







    

   
    
    
    
    
    
    
    
    
    
    
    


































