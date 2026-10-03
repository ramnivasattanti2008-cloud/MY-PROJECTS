from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.wiki_home, name='wiki-home'),
    path('wiki/create/', views.create_page, name='create-page'),
    path('wiki/<slug:slug>/', views.page_view, name='page-view'),
    path('wiki/<slug:slug>/edit/', views.edit_page, name='edit-page'),
    path('wiki/<slug:slug>/history/', views.page_history, name='page-history'),
    path('wiki/<slug:slug>/history/<int:version_id>/', views.page_version, name='page-version'),
    path('wiki/<slug:slug>/restore/<int:version_id>/', views.restore_version, name='restore-version'),
    path('search/', views.search_pages, name='search-pages'),
]
