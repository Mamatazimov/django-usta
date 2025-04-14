from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomePageView,DashboardView,DashboardEditView,MastersTamplateView,MastersCategoryTamplateView
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path("", HomePageView.as_view(), name='home'),
    path('ustalar/', MastersTamplateView.as_view(), name='masters'),
    path('ustalar/<ustalar_category>/', MastersCategoryTamplateView.as_view(), name = 'cmasters'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/edit/', DashboardEditView.as_view(), name='dashboard_edit'),
    path('logout/', LogoutView.as_view(), name='logout'),
]