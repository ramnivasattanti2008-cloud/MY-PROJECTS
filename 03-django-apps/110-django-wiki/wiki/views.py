from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Page, PageVersion


def wiki_home(request):
    pages = Page.objects.all()
    return render(request, 'wiki/home.html', {'pages': pages})


def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        slug = request.POST.get('slug') or None
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('create-page')
        if slug:
            if Page.objects.filter(slug=slug).exists():
                messages.error(request, 'A page with this slug already exists.')
                return redirect('create-page')
        page = Page.objects.create(
            title=title,
            content=content,
            author=request.user if request.user.is_authenticated else None
        )
        PageVersion.objects.create(
            page=page,
            title=page.title,
            content=page.content,
            author=page.author,
            version_number=1,
            change_summary='Initial version'
        )
        messages.success(request, 'Page created!')
        return redirect('page-view', slug=page.slug)
    return render(request, 'wiki/edit.html', {'action': 'Create'})


def page_view(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'wiki/page.html', {'page': page})


def edit_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        page.title = request.POST.get('title', page.title)
        page.content = request.POST.get('content', page.content)
        page.save()
        next_version = page.versions.count() + 1
        PageVersion.objects.create(
            page=page,
            title=page.title,
            content=page.content,
            author=request.user if request.user.is_authenticated else None,
            version_number=next_version,
            change_summary=request.POST.get('change_summary', '')
        )
        messages.success(request, 'Page updated!')
        return redirect('page-view', slug=page.slug)
    return render(request, 'wiki/edit.html', {'page': page, 'action': 'Edit'})


def page_history(request, slug):
    page = get_object_or_404(Page, slug=slug)
    versions = page.versions.all()
    return render(request, 'wiki/history.html', {'page': page, 'versions': versions})


def page_version(request, slug, version_id):
    page = get_object_or_404(Page, slug=slug)
    version = get_object_or_404(PageVersion, page=page, version_number=version_id)
    return render(request, 'wiki/version.html', {'page': page, 'version': version})


def restore_version(request, slug, version_id):
    page = get_object_or_404(Page, slug=slug)
    version = get_object_or_404(PageVersion, page=page, version_number=version_id)
    if request.method == 'POST':
        page.title = version.title
        page.content = version.content
        page.save()
        next_version = page.versions.count() + 1
        PageVersion.objects.create(
            page=page,
            title=page.title,
            content=page.content,
            author=request.user if request.user.is_authenticated else None,
            version_number=next_version,
            change_summary=f'Restored to version {version_id}'
        )
        messages.success(request, f'Restored to version {version_id}!')
        return redirect('page-view', slug=page.slug)
    return render(request, 'wiki/restore.html', {'page': page, 'version': version})


def search_pages(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Page.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'wiki/search.html', {'query': query, 'results': results})
