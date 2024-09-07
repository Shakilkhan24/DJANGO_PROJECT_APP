from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ProfileForm, BlogPostForm, CommentForm
from .models import CustomUser, BlogPost, Comment, Tag, BlogPostTag
from django.contrib import messages
from .forms import CustomUserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserEditForm


class CustomLoginView(LoginView):
    template_name = 'app/login.html'  # Adjust this path based on your structure

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')  # Redirect to profile creation page
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})


@login_required
def profile_creation(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('blog_list')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'app/profile.html', {'form': form})


@login_required
def user_profile(request):
    return render(request, 'app/user_profile.html')


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'app/profile_edit.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    # Perform any additional actions here
    return redirect('home')  # Redirect to the home page or another URL

def blog_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'app/blog_list.html', {'blog_posts': blog_posts}) 



from django.contrib.auth import get_user_model
@login_required
def blog_create(request):
    CustomUser = get_user_model()
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = CustomUser.objects.get(id=request.user.id)
            blog_post.save()
            return redirect('home')  # Change this line from 'blog_list' to 'home'
    else:
        form = BlogPostForm()
    return render(request, 'app/blog_create.html', {'form': form})

@login_required
def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(blog_post=blog_post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'app/blog_detail.html', {
        'blog_post': blog_post,
        'comments': comments,
        'form': form
    })



def blog_edit(request, pk):
    blog_post = BlogPost.objects.get(pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'app/blog_edit.html', {'form': form})

def blog_delete(request, pk):
    blog_post = BlogPost.objects.get(pk=pk)
    blog_post.delete()
    return redirect('blog_list')

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'app/tag_list.html', {'tags': tags})

def tag_detail(request, pk):
    tag = Tag.objects.get(pk=pk)
    blog_posts = BlogPost.objects.filter(blogposttag__tag=tag)
    return render(request, 'app/tag_detail.html', {'tag': tag, 'blog_posts': blog_posts})

def search(request):
    query = request.GET.get('q')
    blog_posts = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(content__icontains=query) | BlogPost.objects.filter(author__username__icontains=query)
    return render(request, 'app/search.html', {'blog_posts': blog_posts})