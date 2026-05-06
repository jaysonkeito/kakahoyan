from django.shortcuts import render
from .models import MediaItem, MediaCategory

def gallery(request):
    categories = MediaCategory.objects.all()
    selected = request.GET.get('category', '')
    items = MediaItem.objects.all()
    if selected:
        items = items.filter(category__slug=selected)
    return render(request, 'gallery/gallery.html', {
        'categories': categories,
        'items': items,
        'selected_category': selected,
    })
