from django.contrib import admin
from .models import Page, PageVersion


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PageVersion)
class PageVersionAdmin(admin.ModelAdmin):
    list_display = ['page', 'version_number', 'author', 'created_at', 'change_summary']
    list_filter = ['created_at']
    search_fields = ['page__title', 'content', 'change_summary']
