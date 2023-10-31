from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View, ListView, UpdateView
from django.contrib.auth import get_user_model
from blog.models import Article, Comment, Reply
from blog.forms import CreateArticleForm, CommentForm, ReplyForm

User = get_user_model()


class MainPageView(ListView):
    template_name = 'index.html'
    model = Article
    queryset = Article.objects.filter(is_published=True)


class ArticleCreateView(CreateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = CreateArticleForm()
        return render(request, 'create-article.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        form = CreateArticleForm(request.POST, request.FILES)
        if form.is_valid():
            art = Article.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                image=form.cleaned_data['image'],
                is_published=form.cleaned_data['is_published'],
                author=request.user
            )
            art.authors.add(request.user, through_defaults={'is_creator': True})
            return redirect('profile')

        return render(request, 'create-article.html', context={'errors': form.errors})


class CreateCollaborationView(View):
    def get(self, request, article_id):
        return render(request, 'collaborate-article.html', context={'article_id': article_id})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        art_to_collaborate = Article.objects.get(id=request.POST['article_id'])
        user_to_collaborate = User.objects.get(email=request.POST['collaborate_email'])

        user_to_collaborate.article_set.add(art_to_collaborate)
        return redirect('profile')



class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        comment_form = CommentForm()
        reply_form = ReplyForm()
        comments = Comment.objects.prefetch_related(
            Prefetch(lookup='replies', queryset=Reply.objects.all().order_by('create_at'))
        ).all().order_by('create_at')
        return render(request, 'article_detail.html', {
            'article': article,
            'comment_form': comment_form,
            'reply_form': reply_form,
            'comments': comments,
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        comment_form = CommentForm(request.POST)
        reply_form = ReplyForm(request.POST)

        if comment_form.is_valid():
            Comment.objects.create(

                message=comment_form.cleaned_data['message'],
                user=request.user,
                article=get_object_or_404(Article, pk=kwargs['pk']),
            )
            return redirect(request.get_full_path())
        return render(request, 'article_detail.html', context={'errors': comment_form.errors})




class ArticleUpdateView(UpdateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        article = Article.objects.get(pk=kwargs['pk'])
        form = CreateArticleForm(instance=article)
        return render(request, 'create-article.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        article = Article.objects.get(pk=kwargs['pk'])
        form = CreateArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('profile')

        return render(request, 'create-article.html', context={'errors': form.errors})


class ArticleDeleteView(View):

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        print(request.POST.get('article_id'))
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return redirect('profile')
