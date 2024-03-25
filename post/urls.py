from django.views.generic.base import TemplateView
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404,handler500
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import JavaScriptCatalog
from django.contrib.sitemaps import views
from django.conf.urls.static import static
from django.conf import settings

# Adds site header, site title, index title to the admin side.
admin.site.site_header = 'Benchatronics Admin'
admin.site.site_title = 'Admins'
admin.site.index_title = 'BENCHATRONICS'




urlpatterns = [
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain')),
    path("__reload__/", include("django_browser_reload.urls")),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),  #add the robots.
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('',include('posts.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('summernote/', include('django_summernote.urls')),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
handler404 = 'posts.views.handler404'
handler500 = 'posts.views.handler500'

