from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class PostList(ListView):
    model = Post
    ordering = '-createDate'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.save()
        return HttpResponseRedirect('/posts')
    form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

class NewsCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        post.author = Author.objects.get(authorUser=self.request.user)
        return super().form_valid(form)

class ArticleCreate(LoginRequiredMixin, CreateView,  PermissionRequiredMixin):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

class NewsUpdate(LoginRequiredMixin, UpdateView,  PermissionRequiredMixin):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticleUpdate(LoginRequiredMixin, UpdateView,  PermissionRequiredMixin):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(LoginRequiredMixin, DeleteView,  PermissionRequiredMixin):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleDelete(LoginRequiredMixin, DeleteView,  PermissionRequiredMixin):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')