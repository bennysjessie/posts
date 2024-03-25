from django.contrib import admin
from . models import *
from django_summernote.admin import SummernoteModelAdmin



# Register your models here.
admin.site.register(Profile)

#admin.site.register(Ads_txt)


class Easy_BallAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(Easy_Ball, Easy_BallAdmin)

class JavascriptAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('summer_content','tags',)


admin.site.register(Javascript, JavascriptAdmin)



admin.site.register(Shop)




admin.site.register(Health_Profile)

admin.site.register(Past_Question)


admin.site.register(Category)


class PhpAdmin(SummernoteModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ('summer_content','tags')

admin.site.register(Php,PhpAdmin)


class BrainyAdmin(admin.ModelAdmin):
    list_display = ('title','category',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Brainy,BrainyAdmin)

class AcademicAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Academic,AcademicAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','draft',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Article,ArticleAdmin)


class BlogAdmin(SummernoteModelAdmin):# instead of ModelAdmin

    list_display = ('title','category','draft',)
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ('summer_content',)

admin.site.register(Blog, BlogAdmin)

admin.site.register(Flutter)

class HtmlAdmin(SummernoteModelAdmin):# instead of ModelAdmin

    list_display = ('title',)
    summernote_fields = ('tags','summer_content',)

admin.site.register(Html, HtmlAdmin)


class PythonAdmin(SummernoteModelAdmin):# instead of ModelAdmin

    list_display = ('title',)
    summernote_fields = ('tags','summer_content',)

admin.site.register(Python, PythonAdmin)


class HealthAdmin(admin.ModelAdmin):
    list_display = ('title','category',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Health,HealthAdmin)

