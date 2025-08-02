from django.urls import path
from .views import HomePageView,DashboardView,DashboardEditView,MastersTamplateView,MastersCategoryTamplateView,MasterTemplateView,ChatsView
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path("", HomePageView.as_view(), name='home'),
    path('ustalar/', MastersTamplateView.as_view(), name='masters'),
    path('ustalar/<ustalar_category>/', MastersCategoryTamplateView.as_view(), name = 'cmasters'),
    path("usta/<usta_username>/",MasterTemplateView.as_view(),name="master"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/edit/', DashboardEditView.as_view(), name='dashboard_edit'),
    path('chats/',ChatsView.as_view(),name="chats")
]
