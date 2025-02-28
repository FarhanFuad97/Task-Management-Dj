from django import forms
from tasks.models import Task, TaskDetail

#Django Form............
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')

    def  __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees", [])
       
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    """Mixing to apply style to form field"""

     
    def __init__(self,*arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"

                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300  p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                    
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "spacy-y-2",
                    
                })

            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            




#Django Model Form.................
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to'] 
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
        
   


class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes', 'asset']

    def __init__(self,*arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
















        '''Manual Widget'''
        # exclude = ['project', 'is_completed','created_at', 'updated_at']
        
        # widgets ={
        #     'title':forms.TextInput(attrs={
        #         'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         "placeholder": "Enter task title"

        #     }),

        #     'description':forms.TextInput(attrs={
        #         'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         "placeholder": "Describe the task"

        #     }),


            
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': "border-2 border-gray-300  rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
                

        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class': "spacy-y-2",
                

        #     }),
        # }
    


        




    
