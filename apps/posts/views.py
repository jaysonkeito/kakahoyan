from django.shortcuts import render, get_object_or_404
from .models import Post

def posts_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'posts/posts.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'posts/post_detail.html', {'post': post})
