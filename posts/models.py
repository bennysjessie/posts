
from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils import timezone
from django_comments.moderation import CommentModerator
from django_comments_xtd.moderation import  moderator,SpamModerator
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
#from posts.badwords import badwords


class Category(models.Model):
    name = models.CharField(max_length=300,blank=True,null=True)
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse ('index')


class Profile(models.Model):
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True,upload_to='profile_pics')
    bio = models.TextField()
    facebook_url = models.CharField(max_length=400,blank=True,null=True)
    linkeld_url = models.CharField(max_length=400,blank=True,null=True)
    google_url = models.CharField(max_length=400,blank=True,null=True)
    whatapp_url = models.CharField(max_length=400,blank=True,null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse ('index')

class Health_Profile(models.Model):
    user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True,upload_to='profile_pics')
    bio = models.TextField()
    facebook_url = models.CharField(max_length=400,blank=True,null=True)
    linkeld_url = models.CharField(max_length=400,blank=True,null=True)
    google_url = models.CharField(max_length=400,blank=True,null=True)
    whatapp_url = models.CharField(max_length=400,blank=True,null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse ('index')

class Past_Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_min = models.CharField(max_length=30,default='30 mins estimated study time')
    tag = models.CharField(max_length=300,default='Past_Question')
    title = models.TextField(max_length=255,null=True,blank=False)
    topic = models.TextField(null=True,blank=True)
    keyword = models.TextField(blank=True,null=True)
    table_of_content = RichTextUploadingField(blank=False)
    content = RichTextUploadingField(blank=False)
    learning_objective = RichTextUploadingField(blank=True)
    image = models.ImageField(blank=True, null=True)
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("past_detail",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Shop(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUB', 'Published'),
    )
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tag = models.CharField(max_length=300,default='Shop')
    title = models.TextField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True,null=True)
    content = models.TextField(blank=False,null=True)
    image_url = models.URLField(null=True,blank=True)
    link = models.TextField(null=True,blank=True)
    iframe = models.TextField(null=True,blank=True,max_length=1000000)
    image = models.ImageField(blank=True, null=True)
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    #objects = PostManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("shops",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Html(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUB', 'Published'),
    )
    level = models.TextField(default='Easy')
    description = models.TextField(blank=True, null=True,)
    tags = models.TextField(null=True,blank=True)
    title = models.TextField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True,null=True)
    summer_content = models.TextField(blank=True,null=True)
    content = RichTextUploadingField(blank=False,null=True)
    last_updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    #objects = PostManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("html",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



class PythonManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PythonManager,self).filter(draft=False,publish__lte=timezone.now())


class Python(models.Model):
    description = models.TextField(blank=True, null=True,)
    summer_content = models.TextField(blank=True,null=True)
    level = models.CharField(max_length=10,default='Easy')
    tags = models.TextField(null=True,blank=True)
    title = models.TextField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True,null=True)
    content = RichTextUploadingField(blank=True,null=True)
    last_updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=datetime.now,blank=True)
    draft = models.BooleanField(default="False")
    objects = PythonManager()
    tag = TaggableManager()


    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("python",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)






class Easy_Ball(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUB', 'Published'),
    )
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = RichTextField(blank=True)
    title = models.CharField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True,null=True)
    content = models.TextField()
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    #objects = PostManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("ball-detail",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Academic(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_min = models.CharField(max_length=30,default='6 mins')
    description = models.TextField(blank=True, null=True,)
    tag = models.CharField(max_length=300,default='coding')
    title = models.TextField(max_length=255,null=True,blank=False)
    topic = models.TextField(null=True,blank=True)
    keyword = models.TextField(blank=True,null=True)
    table_of_content = RichTextUploadingField(blank=False)
    content = RichTextUploadingField(blank=False)
    learning_objective = RichTextUploadingField(blank=True)
    image = models.ImageField(blank=True, null=True)
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("edu_detail",kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



class PhpManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PhpManager,self).filter(draft=False,publish__lte=timezone.now())

class Php(models.Model):
    level = models.CharField(max_length=30,default='Easy')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300,default='coding')
    title = models.TextField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True, null=True,)
    tags = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True,)
    content = RichTextUploadingField(blank=True, null=True,)
    summer_content = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True)
    updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=False)
    objects = PhpManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("php_detail",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



#this model is for django
class Blog(models.Model):
    level = models.CharField(max_length=30,default='Easy')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tag = TaggableManager()
    category = models.CharField(max_length=300,default='coding')
    title = models.TextField(max_length=255,null=True,blank=False)
    keyword = models.TextField(blank=True, null=True,)
    tags = RichTextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True,)
    content = RichTextUploadingField(blank=True, null=True,)
    summer_content = models.TextField(blank=True)
    url_image = models.URLField(max_length=200, blank=True,null=True)
    image = models.ImageField(blank=True, null=True)
    updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    draft = models.BooleanField(default=False)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("detail",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.title)
            counter = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{orig}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def clean(self):
        if not self.slug and Blog.objects.filter(slug=self.slug).exists():
            raise ValidationError('A blog with this slug already exists.')

    def __str__(self):
        return self.title
    
    @property
    def get_previous_item(self):
        return Blog.objects.filter(slug__lt=self.slug).order_by('-slug').first()
    @property
    def get_next_item(self):
        return Blog.objects.filter(slug__gt=self.slug).order_by('slug').first()
    
class BlogCommentModerator(CommentModerator):
    email_notification = True
    auto_moderate_field = 'publish'
    moderate_after = 365
moderator.register(Blog, BlogCommentModerator)





class FlutterManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(FlutterManager,self).filter(draft=False,publish__lte=timezone.now())

class Flutter(models.Model):

    level = models.CharField(max_length=30,default='Easy')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tag = TaggableManager()
    category = models.CharField(max_length=100,default='coding')
    title = models.TextField(max_length=255, blank=False)
    keyword = models.TextField(blank=True, null=True,)
    tags = RichTextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True,)
    content = RichTextUploadingField(blank=True, null=True,)
    url_image = models.URLField(max_length=200, blank=True,null=True)
    image = models.ImageField(blank=True, null=True)
    updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True, unique=True)
    draft = models.BooleanField(default=False)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    objects = FlutterManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("flutter_detail",kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.title)
            counter = 1
            while Flutter.objects.filter(slug=self.slug).exists():
                self.slug = f"{orig}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def clean(self):
        if not self.slug and Flutter.objects.filter(slug=self.slug).exists():
            raise ValidationError('An article with this slug already exists.')

    def __str__(self):
        return self.title
    
    @property
    def get_previous_item(self):
        return Article.objects.filter(slug__lt=self.slug).order_by('-slug').first()
    @property
    def get_next_item(self):
        return Article.objects.filter(slug__gt=self.slug).order_by('slug').first()

class FlutterCommentModerator(CommentModerator):
    email_notification = True
    auto_moderate_field = 'publish'
    moderate_after = 365
moderator.register(Flutter, FlutterCommentModerator)







class ArticleManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(ArticleManager,self).filter(draft=False,publish__lte=timezone.now())

class Article(models.Model):

    read_min = models.CharField(max_length=30,default='6 mins')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300,default= 'blog')
    title = models.CharField(max_length=255,blank=False,null=True)
    keyword = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    tags = RichTextUploadingField(blank=True, null=True,)
    body = RichTextUploadingField(null=True,blank=False,config_name='special')
    content = RichTextUploadingField(blank=True, null=True,)
    image = models.ImageField(blank=True, null=True)
    url_image = models.URLField(max_length=200, blank=True,null=True)
    updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    draft = models.BooleanField(default=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    objects = ArticleManager()
    tag = TaggableManager()


    class Meta:
        ordering = ('-publish',)

    def get_random():
        return Article.objects.order_by("?").first()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("my_blog",kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.title)
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{orig}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def clean(self):
        if not self.slug and Article.objects.filter(slug=self.slug).exists():
            raise ValidationError('An article with this slug already exists.')

    def __str__(self):
        return self.title
    
    @property
    def get_previous_item(self):
        return Article.objects.filter(slug__lt=self.slug).order_by('-slug').first()
    @property
    def get_next_item(self):
        return Article.objects.filter(slug__gt=self.slug).order_by('slug').first()

# javascript model

class Javascript(models.Model):

    dificulty = models.CharField(max_length=30,default='6 mins')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300,default='coding')
    title = models.TextField(max_length=255, blank=False,null=True)
    keyword = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True,)
    summer_content = models.TextField(blank=True, null=True,)
    content = RichTextUploadingField(blank=True, null=True,)
    publish = models.DateTimeField(default=datetime.now,blank=True)
    date_modified = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    #objects = PostManager()

    class Meta:
        ordering = ('-publish',)



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("javascript",kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)




class Health(models.Model):
    read_min = models.CharField(max_length=30,default='6 mins')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300,default='health tips')
    title = models.TextField(null=True,blank=False)
    keyword = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    date_added = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("health_tips",kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


#This model is for Academics
class Brainy(models.Model):
    read_min = models.CharField(max_length=30,default='6 mins')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300,default='coding')
    title = models.TextField(blank=False,max_length=255,null=True)
    keyword = models.TextField(default='maths,physics,chemistry,engineering',max_length=1000)
    description = models.TextField(blank=True, null=True)
    tag = RichTextField(blank=True,null=True)
    content = RichTextUploadingField(null=True,blank=True)
    summer_content = models.TextField(blank=True, null=True,)
    updated = models.DateTimeField(default=datetime.now,blank=True)
    slug = models.SlugField(max_length=255,blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    publish = models.DateTimeField(default=timezone.now)
    #objects = PostManager()

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("brainhub",kwargs={'slug':self.slug})
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    
    @property
    def get_previous_item(self):
        return Brainy.objects.filter(slug__lt=self.slug).order_by('-slug').first()
    @property
    def get_next_item(self):
        return Brainy.objects.filter(slug__gt=self.slug).order_by('slug').first()
