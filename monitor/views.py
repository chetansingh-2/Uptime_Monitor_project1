from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import StatusCheck,  Website
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WebsiteForm, CustomUserCreationForm
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Min, Max, Count
import json


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



class WebsiteDetailView(DetailView):
    model = Website
    template_name = 'monitor/website_detail.html' 
    context_object_name = 'website'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        website = self.get_object()

        time_range_str = self.request.GET.get('range', '24h')
        if time_range_str == '7d':
            start_date = timezone.now() - timedelta(days=7)
            time_range_label = 'Last 7 Days'
        elif time_range_str == '30d':
            start_date = timezone.now() - timedelta(days=30)
            time_range_label = 'Last 30 Days'
        else: 
            start_date = timezone.now() - timedelta(hours=24)
            time_range_label = 'Last 24 Hours'

        checks_in_range = StatusCheck.objects.filter(
            website=website,
            timestamp__gte=start_date
        ).order_by('timestamp')

        stats = checks_in_range.aggregate(
            avg_response=Avg('response_time'),
            min_response=Min('response_time'),
            max_response=Max('response_time')
        )
        
        # FIX: Pre-calculate the millisecond values here in the view.
        # This prevents doing math in the template, which is not supported.
        if stats.get('avg_response') is not None:
            stats['avg_response_ms'] = stats['avg_response'] * 1000
            stats['min_response_ms'] = stats['min_response'] * 1000
            stats['max_response_ms'] = stats['max_response'] * 1000
        else:
            # Provide default values if no checks exist in the range
            stats['avg_response_ms'] = 0
            stats['min_response_ms'] = 0
            stats['max_response_ms'] = 0

        context['stats'] = stats
        context['time_range_label'] = time_range_label

        # 2. Prepare data for the response time chart
        response_time_data = [
            check.response_time * 1000 if check.is_up and check.response_time is not None else None 
            for check in checks_in_range
        ]
        response_time_labels = [
            check.timestamp.strftime('%H:%M') for check in checks_in_range
        ]
        context['response_time_data_json'] = json.dumps(response_time_data)
        context['response_time_labels_json'] = json.dumps(response_time_labels)

        # 3. Prepare data for the status code pie chart
        status_code_counts = checks_in_range.values('status_code').annotate(count=Count('id')).order_by('status_code')
        
        pie_chart_labels = [str(item['status_code']) if item['status_code'] else 'N/A' for item in status_code_counts]
        pie_chart_series = [item['count'] for item in status_code_counts]

        context['pie_chart_labels_json'] = json.dumps(pie_chart_labels)
        context['pie_chart_series_json'] = json.dumps(pie_chart_series)

        # 4. Paginate the raw check history (ordered newest first)
        # OPTIMIZATION: Reuse the 'checks_in_range' queryset instead of hitting the DB again.
        history_checks = checks_in_range.order_by('-timestamp')
        paginator = Paginator(history_checks, 10) # Show 10 checks per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context
