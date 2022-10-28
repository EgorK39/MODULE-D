from django.urls import path
from .views import Articles, Article, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
    path('', Articles.as_view(), name='articles'),
    path('<int:pk>', Article.as_view(), name='article'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
