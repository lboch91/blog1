from django.shortcuts import render, redirect
from posts.models import Post
from posts.forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all().order_by('-date_posted')  # Sortuje posty od najnowszego do najstarszego
    for post in posts:
        if post.image:
            post.image_url = post.image.url if post.image and hasattr(post.image, 'url') else None
        else:
            post.image_url = None
    return render(request, 'home.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_admin

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user  # Przypisuje bieżącego użytkownika jako autora
            new_post.save()
            return redirect('home')  # Przekierowanie do strony głównej lub innego widoku
    else:
        form = PostForm()
    return render(request, 'posts/add_post.html', {'form': form})

@login_required
def posts_by_category(request, category):
    posts = Post.objects.filter(category=category).order_by('-date_posted')
    return render(request, 'posts/posts_by_category.html', {'posts': posts, 'category': category})


from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatyczne logowanie użytkownika po rejestracji
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')  # Przekierowanie do strony głównej po pomyślnej rejestracji
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


from django.shortcuts import redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('home')  # Zapewnia, że tylko autor może edytować post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
        return redirect('home')
    return redirect('post_detail', post_id=post.id)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    image_url = post.image.url if post.image and hasattr(post.image, 'file') else None
    return render(request, 'posts/post_detail.html', {'post': post, 'image_url': image_url})


from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Przekierowanie do strony logowania po pomyślnej rejestracji
    template_name = 'registration/signup.html'


from django.shortcuts import get_object_or_404


def posts_by_category(request, category):
    posts = Post.objects.filter(category=category).order_by('-date_posted')
    return render(request, 'posts/posts_by_category.html', {'posts': posts, 'category': category})


from django.shortcuts import render
from .models import Post
from .forms import CategoryFilterForm

def post_list(request):
    form = CategoryFilterForm(request.GET)
    if form.is_valid() and form.cleaned_data['category']:
        posts = Post.objects.filter(category=form.cleaned_data['category']).order_by('-date_posted')
    else:
        posts = Post.objects.all().order_by('-date_posted')

    return render(request, 'posts/post_list.html', {'posts': posts, 'form': form})


