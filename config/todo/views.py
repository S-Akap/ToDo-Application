from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views import View
from . import forms, models


class IndexView(generic.TemplateView):
    template_name = 'todo/index.html'



class LogInView(LoginView):
    template_name = 'todo/form.html'
    form_class = forms.LogInForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Log-In'
        return context

class LogOutView(LoginRequiredMixin, LogoutView):
    template_name = 'todo/form.html'

class SignUpView(generic.CreateView):
    template_name = 'todo/form.html'
    form_class = forms.SignUpForm

    def form_valid(self, form):
        user = form.save()
        return redirect('todo:signup_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Sign-Up'
        return context

class SignUpDoneView(generic.TemplateView):
    template_name = 'todo/signup_done.html'



class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['classes'] = models.Class.objects.filter(user=user)[:3]
        context['tasks'] = models.Task.objects.filter(class_reference__user=user, is_completed=False)[:3]
        context['is_home'] = True
        return context



class AccountMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']

class AccountView(AccountMixin, generic.DetailView):
    model = User
    template_name = 'todo/account_detail.html'

class AccountUpdateView(AccountMixin, generic.UpdateView):
    model = User
    form_class = forms.AccountUpdateForm
    template_name = 'todo/form.html'

    def get_success_url(self):
        return resolve_url('todo:account', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Edit Account'
        return context

class PasswordUpdateView(AccountMixin, PasswordChangeView):
    form_class = forms.PasswordUpdateForm
    success_url = reverse_lazy('todo:account')
    template_name = 'todo/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Change Password'
        return context

class AccountDeleteView(AccountMixin, generic.DeleteView):
    model = User
    template_name = 'todo/account_delete.html'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class ClassListView(generic.ListView):
    model = models.Class
    template_name = 'todo/list.html'
    context_object_name = 'classes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['classes'] = models.Class.objects.filter(user=user)
        context['is_class_list'] = True
        return context

class ClassDetailView(generic.DetailView):
    model = models.Class
    template_name = 'todo/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_instance = self.get_object()
        context['tasks'] = models.Task.objects.filter(class_reference=class_instance)
        return context

class ClassCreateView(generic.CreateView):
    model = models.Class
    form_class = forms.ClassForm
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo:class_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Create Class'
        return context

class ClassUpdateView(generic.UpdateView):
    model = models.Class
    form_class = forms.ClassForm
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo:class_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Edit Class'
        return context

class ClassDeleteView(generic.DeleteView):
    model = models.Class
    template_name = 'todo/class_delete.html'
    success_url = reverse_lazy('todo:class_list')



class TaskListView(generic.ListView):
    model = models.Task
    template_name = 'todo/list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['tasks'] = models.Task.objects.filter(class_reference__user=user)
        context['is_task_list'] = True
        return context

class TaskDetailView(generic.DetailView):
    model = models.Task
    template_name = 'todo/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(generic.CreateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Create Task'
        return context

class TaskUpdateView(generic.UpdateView):
    model = models.Task
    form_class = forms.TaskUpdateForm
    template_name = 'todo/form.html'
    success_url = reverse_lazy('todo:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['process_name'] = 'Update Task'
        return context

class TaskDeleteView(generic.DeleteView):
    model = models.Task
    template_name = 'todo/task_delete.html'
    success_url = reverse_lazy('todo:task_list')

class TaskCreateWithClassView(View):
    def get(self, request, *args, **kwargs):
        class_form = forms.ClassForm()
        task_form = forms.TaskForm()
        return render(request, 'todo/task_with_class_form.html', {
            'class_form': class_form,
            'task_form': task_form
        })

    def post(self, request, *args, **kwargs):
        class_form = forms.ClassForm(request.POST)
        task_form = forms.TaskForm(request.POST)
        if class_form.is_valid() and task_form.is_valid():
            new_class = class_form.save(commit=False)
            new_class.user = request.user
            new_class.save()
            task_form.instance.class_reference = new_class
            new_task = task_form.save(commit=False)

            new_task.save()
            return redirect(reverse_lazy('todo:task_list'))
        return render(request, 'todo:task_with_class_form.html', {
            'class_form': class_form,
            'task_form': task_form
        })