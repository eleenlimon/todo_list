from django.shortcuts import render, HttpResponse, redirect
from .models import Task
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

class TaskLoginView(LoginView):
    template_name = "todo/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task_list")


# create a form, create a link to Register/ make an account

class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    # redirect the user once the form is filled/submitted, make sure the user is logged in
    def form_valid(self, form):
        user = form.save()  # saves the form to be able to log in
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):  # able to request the user to access the register pg once LOGGED in
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # task_list.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # getting only user tasks
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()  # if marked not complete will give number

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)  # filters out the tasks
            context['search_input'] = search_input
        return context  # enables user to search, once searched, the input is still displayed


# create a search form, able to search tasks (the logic)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    # task_detail.html


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = reverse_lazy('task_list')
    fields = ['title', 'description', 'complete',
              'created']  # want all the fields excpet the user , task_form.html (have to create path in task_list)

    # in html- create form, + csrf token, once form is created it will prompt back to task_list

    def form_valid(self, form):  # this ensures that task created is only for the user
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy('task_list')
    fields = ['title', 'description', 'complete', 'created']


# create a back link on form.html , add a edit link on task_list.html

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    context_object_name = 'task'  # allows you to call the tasks in html by 'tasks'
    # no template needed here its task_confirm_delete, add delete to task_list.html (create a form),add go back
