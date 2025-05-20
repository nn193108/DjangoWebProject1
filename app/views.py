"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .forms import FeedbackForm, CommentForm, BlogForm
from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Comment
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    """Render the home page."""
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'year': datetime.now().year,
        }
    )

def pool(request):
    """Improved feedback form handling."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Prepare display values
            rating_map = {
                '5': 'Отлично',
                '4': 'Хорошо',
                '3': 'Удовлетворительно',
                '2': 'Плохо',
                '1': 'Очень плохо'
            }
            
            frequency_map = {
                'daily': 'Ежедневно',
                'weekly': 'Еженедельно',
                'monthly': 'Ежемесячно',
                'rarely': 'Редко',
                'first': 'Впервые'
            }
            
            improvements_map = {
                'design': 'Дизайн',
                'content': 'Содержание',
                'navigation': 'Навигацию',
                'speed': 'Скорость работы',
                'mobile': 'Мобильную версию'
            }
            
            context = {
                'title': 'Обратная связь',
                'message': 'Спасибо за ваш отзыв',
                'year': datetime.now().year,
                'data': {
                    **data,
                    'site_rating_display': rating_map.get(data['site_rating'], ''),
                    'visit_frequency_display': frequency_map.get(data['visit_frequency'], ''),
                    'improvements_display': [improvements_map.get(opt, '') 
                                          for opt in data.get('improvements', [])],
                },
                'form': None
            }
            return render(request, 'app/pool.html', context)
        
        return render(
            request,
            'app/pool.html',
            {
                'title': 'Обратная связь',
                'year': datetime.now().year,
                'form': form
            }
        )
    
    return render(
        request,
        'app/pool.html',
        {
            'title': 'Обратная связь',
            'year': datetime.now().year,
            'form': FeedbackForm()
        }
    )

def registration(request):
    """Improved registration view."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            user = regform.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        regform = UserCreationForm()
    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders blog posts with pagination."""
    posts = Blog.objects.exclude(title="Video Comments").order_by('-posted')
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, post_id):
    """Improved blog post view with better error handling."""
    post = get_object_or_404(Blog, id=post_id)
    comments = Comment.objects.filter(post=post).exclude(post__title="Video Comments")
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blogpost', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(
        request,
        'app/blogpost.html',
        {
            'title': post.title,
            'post': post,
            'form': form,
            'comments': comments,
            'year': datetime.now().year,
        }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def newpost(request):
    """Improved new post creation."""
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect('blog')
    else:
        form = BlogForm()
    
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Добавить статью блога',
            'form': form,
            'year': datetime.now().year,
        }
    )

def video(request):
    """Improved video comments handling."""
    video_post, created = Blog.objects.get_or_create(
        title="Video Comments",
        defaults={
            'description': "Comments on the video page",
            'content': "This post contains comments related to the video page.",
            'author': request.user if request.user.is_authenticated else None
        }
    )
    
    comments = Comment.objects.filter(post=video_post).order_by('-date')
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = video_post
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('video')
    else:
        form = CommentForm()
    
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'form': form,
            'comments': comments,
            'year': datetime.now().year,
        }
    )