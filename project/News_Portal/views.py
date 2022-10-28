from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter, PostFilter2
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404  # !
from django.contrib.auth.decorators import login_required
from .tasks import *


class News(ListView):
    model = Post
    # ordering = '-time_in'
    # queryset = Post.objects.order_by('-time_in')
    queryset = Post.objects.filter(Wahl='Nachricht')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context


class Articles(ListView):
    model = Post
    # ordering = '-time_in'
    # queryset = Post.objects.order_by('-time_in')
    queryset = Post.objects.filter(Wahl='Artikel')
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 2


class Search(ListView):
    model = Post
    queryset = Post.objects.order_by('-time_in')
    template_name = 'search.html'
    context_object_name = 'search'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter2(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class New(DetailView):
    model = Post
    queryset = Post.objects.filter(Wahl='Nachricht')
    template_name = 'new.html'
    context_object_name = 'new'


class Article(DetailView):
    model = Post
    queryset = Post.objects.filter(Wahl='Artikel')
    template_name = 'article.html'
    context_object_name = 'article'


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('News_Portal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.Wahl = 'Nachricht'
        notify_new_post.delay()  # form.instance.email
        return super().form_valid(form)

    # def form_valid(self, form):
    #     form.save()
    #     notify_new_post.delay(form.instance.email)
    #     return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('News_Portal.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.Wahl = 'Artikel'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News_Portal.add_change',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('News_Portal.add_change',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('News_Portal.add_delete',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('News_Portal.add_delete',)
    raise_exception = True
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles')


# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'post_edit.html', {'form': form})
# Create your views here.

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def sub(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались '
    return render(request, 'sub.html', {'category': category, 'message': message})
