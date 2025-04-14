from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from .form import ProfileForm, UserForm, PostForm, CategoryForm
from .models import Profile, Post, MatersCategory
from register.models import CustomUser
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = MatersCategory.objects.values_list('name',flat=True)
        return context

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = Profile.objects.get(user=user)
        context['user'] = CustomUser.objects.get(username=user)
        context['posts'] = Post.objects.filter(user=user)
        context['category'] = Profile.objects.get(user=user).m_category

        return context
    

class DashboardEditView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
        post_form = PostForm()
        posts = Post.objects.filter(user=user)
        logo = Profile.objects.get(user=user).avatar
        user_status = CustomUser.objects.get(username=user).user_status
        category_form = CategoryForm()
        return render(request, 'dashboard-edit.html', {'profile_form': profile_form, 'user_form': user_form, 'logo': logo,"post_form":post_form,"posts":posts,'status':user_status,'category':category_form})
    
    def post(self, request):
        user = self.request.user
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        post_form = PostForm(request.POST , request.FILES)
        logo = Profile.objects.get(user=user).avatar
        posts = Post.objects.filter(user=user)
        user_status = CustomUser.objects.get(username=user).user_status
        category_form = CategoryForm()



        if profile_form.is_valid() and user_form.is_valid() and post_form.is_valid():
            profile_form.save()
            user_form.save()
            post = post_form.save(commit=False)
            post.user = request.user
            photo = request.POST.get('photo')
            removing_posts = request.POST.getlist('post_ids')
            Post.objects.filter(id__in=removing_posts, user=user).delete()
            
            if request.POST.get("selected_option"):
                print(request.POST.get("selected_option"))

                category_id = int(request.POST.get("selected_option"))
                print(category_id)
                Profile.objects.filter(user = user).update(m_category_id = category_id)
            
            if photo != "":
                post.save()
            return redirect('dashboard')
        

        return render(request, 'dashboard-edit.html', {'profile_form': profile_form, 'user_form': user_form,"post_form":post_form, 'logo': logo,"posts":posts,"msg":"Iltimos ma'lumotlarni to'g'ri kiriting!",'status':user_status})
    
class MastersTamplateView(TemplateView):
    template_name = 'masters.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = CustomUser.objects.filter(user_status=1 or True)
        context['profile'] = Profile.objects.filter(user__user_status=1 or True)

        ex_list = []
        for i in context['user']:
            ex_list.append([i.username,i.date_joined,context['profile'].get(user_id = i.id).avatar,context['profile'].get(user_id = i.id).bio])


        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(ex_list, 24)
        page_obj = paginator.get_page(page_number)

        context['mainList'] = page_obj
        context['currentPage'] = int(page_number)

        return context

class MastersCategoryTamplateView(TemplateView):
    template_name = 'masters.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cmaster = self.kwargs.get('ustalar_category')
        context['user'] = CustomUser.objects.filter(user_status=1 or True)
        context['profile'] = Profile.objects.filter(user__user_status=1 or True)

        ex_list = []
        for i in context['user']:
            if str(context['profile'].get(user_id = i.id).m_category).lower() == str(cmaster).lower():
                ex_list.append([i.username,i.date_joined,context['profile'].get(user_id = i.id).avatar,context['profile'].get(user_id = i.id).bio])


        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(ex_list, 24)
        page_obj = paginator.get_page(page_number)

        context['mainList'] = page_obj
        context['currentPage'] = int(page_number)

        return context


