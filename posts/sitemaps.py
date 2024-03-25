from django.contrib.sitemaps import Sitemap
from .models import Shop, Article, Html,Blog, Python, Easy_Ball,Brainy,Health,Flutter
from django.urls import reverse


class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Blog.objects.filter()
    def lastmod(self,obj):
        return obj.updated


class FlutterSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Flutter.objects.filter()
    def lastmod(self,obj):
        return obj.updated



class HtmlSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Html.objects.filter()
    def lastmod(self,obj):
        return obj.publish


class PythonSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Python.objects.filter()
    def lastmod(self,obj):
        return obj.last_updated



class ShopSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Shop.objects.filter()
    def lastmod(self,obj):
        return obj.date_added

class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Article.objects.filter()
    def lastmod(self,obj):
        return obj.updated


class BrainySitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Brainy.objects.filter()
    def lastmod(self,obj):
        return obj.updated



class Easy_BallSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Easy_Ball.objects.filter()
    def lastmod(self,obj):
        return obj.date_added

class HealthSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return Health.objects.filter()
    def lastmod(self,obj):
        return obj.date_added



class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority=0.9
    def items(self):
        return ('category','login','signup','index',)
    def location(self, item):
        return reverse(item)




class GeneralSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['sitemap_blog', 'sitemap_article','sitemap_flutter',
                'sitemap_health','sitemap_shop','sitemap_easy_ball',
                'sitemap_python','sitemap_brainy','sitemap_static','sitemap_html'
                ]  # These are keys to reference the specific sitemaps

    def location(self, item):
        return reverse(item)  # Reverse the URL name to get the URL