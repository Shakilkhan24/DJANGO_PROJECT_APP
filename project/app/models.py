from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission 

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    short_bio = models.TextField(blank=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set'  # Specify a custom related_name
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set'  # Specify a custom related_name
    )

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=255)

class BlogPostTag(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
