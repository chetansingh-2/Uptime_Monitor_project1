from django.urls import path
from .views import (WebsiteListView, WebsiteCreateView, WebsiteUpdateView, WebsiteDeleteView, SignupView, WebsiteDetailView)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', WebsiteListView.as_view(), name='website-list'),
    path('site/add/', WebsiteCreateView.as_view(), name='website-add'),
    path('site/<int:pk>/update/', WebsiteUpdateView.as_view(), name='website-update'),
    path('site/<int:pk>/delete/', WebsiteDeleteView.as_view(), name='website-delete'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('site/<int:pk>/details/', WebsiteDetailView.as_view(), name='website-detail'),


]
