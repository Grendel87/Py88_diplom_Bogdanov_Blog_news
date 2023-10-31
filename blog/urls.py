from django.urls import path

from blog.views import MainPageView, ArticleCreateView, CreateCollaborationView, ArticleUpdateView, ArticleDeleteView, \
    ArticleDetailView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('create-article/', ArticleCreateView.as_view(), name='create_article'),
    path('create-collaboration/', CreateCollaborationView.as_view(), name='create_collaboration'),
    path('collaborate-article/<int:article_id>/', CreateCollaborationView.as_view(), name='create_collaboration'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('update-article/<int:pk>/', ArticleUpdateView.as_view(), name='update-article'),
    path('delete-article/', ArticleDeleteView.as_view(), name='articles_delete'),
]
