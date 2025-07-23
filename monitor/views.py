from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import StatusCheck,  Website
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WebsiteForm, CustomUserCreationForm



class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class WebsiteCreateView(LoginRequiredMixin, CreateView):
    model = Website
    form_class = WebsiteForm
    template_name = 'monitor/website_form.html'
    success_url = reverse_lazy('website-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WebsiteUpdateView(LoginRequiredMixin, UpdateView):
    model = Website
    form_class = WebsiteForm
    template_name = 'monitor/website_form.html'
    success_url = reverse_lazy('website-list')

    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).order_by('name')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WebsiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Website
    template_name = 'monitor/website_confirm_delete.html'
    success_url = reverse_lazy('website-list')
    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).order_by('name')



class WebsiteListView(LoginRequiredMixin, ListView):

    # 1. Tell the view which model to get data from.
    # Django will automatically do `Website.objects.all()` in the background for us.

    model = Website
    
    # 2. Specify which template file to use for displaying the page.
    template_name = 'monitor/website_list.html'

    # 3. Define the name of the variable we will use in the template.
    # By default, Django calls it 'object_list'. 'websites' is much clearer.
    context_object_name = 'websites'

    def get_queryset(self):
        return Website.objects.filter(user=self.request.user).order_by('name')