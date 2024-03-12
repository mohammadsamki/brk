from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Task  # or from other_app.models import Task

 
class TaskSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        # Return all Task objects, or whatever objects you want to include in the sitemap.
        return Task.objects.all()

    def location(self, item):
        # Return the URL for each item.
        return reverse('task_detail', args=[item.pk])

class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return [ 'home', 'register']

    def location(self, item):
        return reverse(item)
