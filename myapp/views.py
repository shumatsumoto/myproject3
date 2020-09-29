from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm


class Index(TemplateView):
	template_name = 'myapp/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post_list = Post.objects.all().order_by('-created_at')
		context = {
			'post_list': post_list,
		}
		return context


class PostCreate(CreateView):
	model = Post
	form_class = PostForm
	success_url = reverse_lazy('myapp:index')


class PostDetail(DetailView):
	model = Post
