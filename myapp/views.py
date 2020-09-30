from django.shortcuts import render, resolve_url
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(TemplateView):
	template_name = 'myapp/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post_list = Post.objects.all().order_by('-created_at')
		context = {
			'post_list': post_list,
		}
		return context


class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	success_url = reverse_lazy('myapp:index')

	def form_valid(self, form):
		form.instance.author_id = self.request.user.id
		return super(PostCreate, self).form_valid(form)
	
	def get_success_url(self):
		messages.success(self.request, 'Postを登録しました。')
		return resolve_url('myapp:index')


class PostDetail(DetailView):
	model = Post


class PostUpdate(LoginRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm

	def get_success_url(self):
		messages.info(self.request, 'Postを更新しました。')
		return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(LoginRequiredMixin, DeleteView):
	model = Post

	def get_success_url(self):
		messages.info(self.request, 'Postを削除しました。')
		return resolve_url('myapp:index')


class PostList(ListView):
	model = Post

	def get_queryset(self):
		return Post.objects.all().order_by('-created_at')
	

class Login(LoginView):
	form_class = LoginForm
	template_name = 'myapp/login.html'


class Logout(LogoutView):
	template_name = 'myapp/logout.html'


class SignUp(CreateView):
	form_class = SignUpForm
	template_name = 'myapp/signup.html'
	success_url = reverse_lazy('myapp:index')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		self.object = user
		messages.info(self.request, 'ユーザー登録をしました。')
		return HttpResponseRedirect(self.get_success_url())
