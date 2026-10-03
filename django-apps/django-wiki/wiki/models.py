from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import markdown


class Page(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_html_content(self):
        return markdown.markdown(self.content, extensions=['markdown.extensions.fenced_code'])


class PageVersion(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    version_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    change_summary = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-version_number']
        unique_together = ('page', 'version_number')

    def __str__(self):
        return f'{self.page.title} v{self.version_number}'

    def get_html_content(self):
        return markdown.markdown(self.content, extensions=['markdown.extensions.fenced_code'])
