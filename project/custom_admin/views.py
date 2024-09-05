from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from app.models import BlogPost, Comment, Category, Tag, BlogPostTag
from app.forms import BlogPostForm, ProfileForm
from django.db.models import Count

from django.db.models import Count
from django.contrib.auth import get_user_model

def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def user_list(request):
    User = get_user_model()
    try:
        users = User.objects.all()
        for user in users:
            user.post_count = BlogPost.objects.filter(author=user).count()
        return render(request, 'custom_admin/user_list.html', {'users': users})
    except Exception as e:
        print(f"Error in user_list view: {str(e)}")
        # You might want to render an error template here
        return render(request, 'custom_admin/error.html', {'error': str(e)})
@user_passes_test(is_admin)
def dashboard(request):
    User = get_user_model()
    context = {
        'total_users': User.objects.count(),
        'total_posts': BlogPost.objects.count(),
        'total_comments': Comment.objects.count(),
        'recent_posts': BlogPost.objects.order_by('-created_at')[:5],
        'recent_comments': Comment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'custom_admin/dashboard.html', context)


@user_passes_test(is_admin)
def blog_post_list(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/blog_post_list.html', {'blog_posts': blog_posts})

@user_passes_test(is_admin)
def blog_post_edit(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('custom_admin_blog_post_list')
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'custom_admin/blog_post_edit.html', {'form': form, 'blog_post': blog_post})

@user_passes_test(is_admin)
def blog_post_delete(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        blog_post.delete()
        return redirect('custom_admin_blog_post_list')
    return render(request, 'custom_admin/blog_post_delete.html', {'blog_post': blog_post})

@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.annotate(post_count=Count('blogpost'))
    return render(request, 'custom_admin/category_list.html', {'categories': categories})

@user_passes_test(is_admin)
def tag_list(request):
    tags = Tag.objects.annotate(post_count=Count('blogposttag'))
    return render(request, 'custom_admin/tag_list.html', {'tags': tags})