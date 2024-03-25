from typing import Optional
from taggit.models import Tag #import at top
from . forms import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . models import *
from django.db.models import Q
from django.contrib.auth import authenticate,login
from django.http import HttpResponse,JsonResponse
from django.views.generic import CreateView,UpdateView,DeleteView,ListView
from django.shortcuts import render,get_object_or_404, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import FormView, TemplateView
import webbrowser
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .models import *
from django.template.defaultfilters import truncatechars
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.core.mail import EmailMultiAlternatives

"""
Leave the three to four functions here they are for checking user pass test i have written for function based view and classbased view,
you just need to apply it at the head of each view function while in clss base view you have to include it inside the view it self
"""
def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url='account_login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


#for admin_required
def admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url='account_login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

#class base test for user pass test, you can also rewrite it for staff, user and supper user
class SuperUsercheck(UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

class AdminUserCheck(UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_staff


def get_titles(request):
    titles_data = [{'title': truncatechars(blog.title, 40), 'url': reverse('detail', args=[blog.slug])} for blog in Blog.objects.all()]
    return JsonResponse(titles_data, safe=False)

"""
You can use this approach to check if user is admin or staff or ordinary user for function base but
you should know thta django wont redirect the user to login , the draw back here is that the user would be redirected many times.
"""
#@user_passes_test(lambda u: u.is_staff)


def search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    if form.is_valid():
        search_query = form.cleaned_data['search_query']

        # Search in Model1
        blog_results = Blog.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        results.extend(blog_results)

        # Search in Model2
        article_results = Article.objects.filter(Q(content__icontains=search_query) | Q(title__icontains=search_query))
        results.extend(article_results)

        # Search in Model2
        flutter_results = Flutter.objects.filter(Q(content__icontains=search_query) | Q(title__icontains=search_query))
        results.extend(flutter_results)

            # Search in Model2
        brainy_results = Brainy.objects.filter(Q(content__icontains=search_query) | Q(title__icontains=search_query))
        results.extend(brainy_results)

    context = {
        'results': results,
        'form': form,
    }

    return render(request, 'search_results.html', context)




def Html_Views(request):
    htmls = Html.objects.all()
    context = {'htmls':htmls}
    return render(request,'php_list.html',context)


def PhpListView(request):
    phps = Php.objects.all()
    p = Paginator(phps, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}

    return render(request,'php_list.html',context)

def Php_Detail(request,slug):
    phps = Php.objects.all()
    php = Php.objects.get(slug=slug)

    context = {'php':php,'phps':phps,}
    return render(request,'php_detail.html', context)



def PythonListView(request):
    python = Python.objects.active()
    drafttrue = Python.objects.filter(draft=True)

    p = Paginator(python, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'page_obj':page_obj,'python':python,'drafttrue':drafttrue,}

    return render(request,'python-list.htm',context)

def AboutView(request):
    return render(request,'about.html')

def Lesson_View(request):
    return render(request,'lesson.html')

def Guestpost_View(request):
    return render(request,'guest_post.html')


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

# contact suucess view
class ContactSuccessView(TemplateView):
    template_name = 'success.html'

def join_us(request):
    return render(request,'login_page.html')


def login_user(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"

    if request.user_agent.device.family:
        pass

    if request.user_agent.device:
        pass

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    details = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type":os_type,
        "os_version":os_version
       }

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        context={'username':username,
                  'login_status':True,


       }
        response = redirect('/',context)
        response.set_cookie('username',username)
        response.set_cookie('login_status',True)

        if user is not  None:
            user_email = user.email
            send_login_email(user_email,username)
            auth.login(request, user)
            messages.info(request,'You have successfully logged in')
            return response
        else:
            messages.error(request,'bad credentials')
            return redirect('login')


    return render(request,"login.html",details)

def send_login_email(user_email,username):
    context = {
        'username':username
    }
    subject = 'Welcome to benchatronics.com'
    html_message = render_to_string('user_email_login.html',context)
    plain_message = strip_tags(html_message)
    from_email = 'noreply <noreply@benchatronics.com>'
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    #triger the sending by calling this view any where you want it


#ASKQUESTION
@login_required(login_url='account_login')
def askquest(request):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # pass the object as instance in form
    form= MathsForm(request.POST or None)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('maths')

    # add form dictionary to context
    context= {'form':form}

    return render(request, "ask.html", context)

def first_semester(request):

    first_semester = Academic.objects.all()
    context = {'first_semester':first_semester

        }
    return render(request,'first_semester.html',context)

#ASKQUESTION
@login_required(login_url='account_login')
def askquestion(request):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # pass the object as instance in form
    form= Ask_QuestForm(request.POST or None)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('maths')

    # add form dictionary to context
    context= {'form':form}

    return render(request, "ask_question.html", context)

# question detail view
def Past_QuestionView(request):
    past_list = Past_Question.objects.all()
    context = {'past_list':past_list}
    return render(request,'past_questions.html', context)

def Ball_View(request):
    ball = Easy_Ball.objects.all()
    context = {'ball':ball}
    return render(request,'ball-list.html', context)

def Shop_View(request):
    shop = Shop.objects.all()
    context = {'shop':shop}
    return render(request,'shop.html',context)


# question detail view
def Past_Detail(request,slug):
    past_list = Past_Question.objects.all()
    detail = Past_Question.objects.filter(slug=slug)

    if detail.exists():
        detail = detail.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'past_list':past_list,'detail':detail}
    return render(request,'past_detail.html', context)

def Shop_Detail(request,slug):
    shop = Shop.objects.all()
    shops = Shop.objects.filter(slug=slug)

    if shops.exists():
        shops= shops.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'shops':shops,'shop':shop,}
    return render(request,'shops.html', context)



def Html_View(request,slug):
    htmls = Html.objects.all()
    html = Html.objects.filter(slug=slug)

    if html.exists():
        html= htmls.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'htmls':htmls,'html':html,}
    return render(request,'html.html', context)


def Python_View(request,slug):
    python = Python.objects.all()
    #for recents post
    posts = Python.objects.all()[:10]
    pythons = Python.objects.filter(slug=slug).filter(draft=False)

    if pythons.exists():
        pythons= pythons.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    p = Paginator(python, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'pythons':pythons,'page_obj': page_obj,'posts':posts,}
    return render(request,'python.html', context)





# question detail view
def edu_detail(request,slug):
    first_semester = Academic.objects.all()
    one_semester = Academic.objects.filter(slug=slug)
    if one_semester.exists():
        one_semester = one_semester.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'one_semester':one_semester,'first_semester':first_semester}
    return render(request,'edu_detail.html', context)

def Ball_Detail(request,slug):
    posts=Article.objects.all()
    ball = Easy_Ball.objects.all()
    ball_detail = Easy_Ball.objects.filter(slug=slug)
    if ball_detail.exists():
        ball_detail = ball_detail.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'ball_detail':ball_detail,'ball':ball,'posts':posts}
    return render(request,'ball-detail.html', context)



def PasswordChangedView(request):
    return render(request,'password_changed.html')

class ChangePasswordView(PasswordChangeView):
    form_class= ChangePasswordForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_changed')

class UserEditView(generic.UpdateView):
    form_class= EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user


@login_required
def ProfileView(request):
    post = Article.objects.filter(draft=True).order_by('-updated')
    tips=Health.objects.all()
    skul=Brainy.objects.all()
    cats=Category.objects.all()
    posts=Blog.objects.all()
    context = {'posts':posts,'cats':cats,'skul':skul,'tips':tips,'post':post}
    return render(request, 'my_profile.html', context)

# update of health post
@staff_member_required
def UpdateHealthPostView(request, slug):
    # dictionary for initial data with
    # field names as keys
    tips=Health.objects.all()
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Health, slug = slug)

    # pass the object as instance in form
    form = UpdateHealthPostForm(request.POST or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.info(request,"Your post have been updated succesfuly,Edit again?")

    # add form dictionary to context
    context= {'form':form,'tips':tips}

    return render(request, "edit_health_post.html", context)


# update of python post

@staff_member_required
def UpdatePythonView(request, slug):
    # dictionary for initial data with
    # field names as keys
    python=Python.objects.all()
    context ={}

    # fetch the object related to passed id
    obj = get_object_or_404(Python, slug = slug)

    # pass the object as instance in form
    form = UpdatePythonForm(request.POST or None, instance = obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.info(request,"Your post have been updated succesfuly,Edit again?")

    # add form dictionary to context
    context= {'form':form,'python':python}

    return render(request, "edit_python.html", context)



#health post
def HealthPost(request):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # pass the object as instance in form
    form= HealthPostForm(request.POST or None)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('index')

    # add form dictionary to context
    context= {'form':form}

    return render(request, "addhealthpost.html", context)

def AcademicPost(request):
    # dictionary for initial data with
    # field names as keys
    context ={}

    # pass the object as instance in form
    form= AcademicForm(request.POST or None)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('index')

    # add form dictionary to context
    context= {'form':form}

    return render(request, "add_academic.html", context)


# form for deleting Blog Post

class DeletePostView(SuperUsercheck,DeleteView):
    model = Blog
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')

# form for deleting Blog

class DeleteArticlePostView(SuperUsercheck,DeleteView):
    model = Article
    template_name = 'delete_blog.html'
    success_url = reverse_lazy('index')


class DeleteHealthPostView(SuperUsercheck,DeleteView):
    model = Health
    template_name = 'delete_health_post.html'
    success_url = reverse_lazy('index')

# form for deleting school Post
class DeleteSchoolPostView(LoginRequiredMixin,DeleteView):
    model = Brainy
    template_name = 'delete_school_post.html'
    success_url = reverse_lazy('my_profile')

class AddPostView(AdminUserCheck,CreateView):
    model = Blog
    template_name = 'addpost.html'
    #fields = ('title','content','date_added','slug',)
    form_class = PostForm




class AddFlutterView(SuperUsercheck,CreateView):
    model = Flutter
    template_name = 'add_flutter.html'
    #fields = ('title','content','date_added','slug',)
    form_class = FlutterForm



class AddPhpView(SuperUsercheck,CreateView):
    model = Php
    template_name = 'add_php.html'
    form_class = PhpForm


class AddPyView(SuperUsercheck,CreateView):
    model = Python
    template_name = 'add_py.html'
    form_class = PyForm


class AddBallView(SuperUsercheck,CreateView):
    model = Easy_Ball
    template_name = 'add_ball.html'
    #fields = ('title','content','date_added','slug',)
    form_class = BallForm



@login_required(login_url='account_login')
def admin_article_view(request):
    if request.user.is_superuser:
        form = AdminArticleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request,"Your post have been posted succesfully add another one ?")
        return render(request,'admin_article_template.html',{'form':form})
    else:
        form = UserArticleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request,"Your post have been posted succesfully add another one ?")
        return render(request, 'user_article_template.html',{'form':form})

@login_required(login_url='account_login')
def user_article_view(request):
    if not request.user.is_superuser:
        form = UserArticleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request,"Your post have been posted succesfully add another one ?")
        return render(request,'user_article_template.html',{'form':form})
    else:
        form = AdminArticleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request,"Your post have been posted succesfully add another one ?")
        return render(request, 'admin_article_template.html',{'form':form})


class AddSchoolPostView(AdminUserCheck,CreateView):
    model = Brainy
    template_name = 'addschoolpost.html'
    #fields = ('title','content','date_added','slug',)
    form_class = SchoolPostForm

class UpdatePastView(LoginRequiredMixin,UpdateView):
    model = Past_Question
    template_name = 'edit_past.html'
    fields = '__all__'
    #success_url = reverse_lazy('past_detail')


class Update_Flutter(SuperUsercheck,UpdateView):
    model = Flutter
    template_name = 'edit_flutter.html'
    fields = '__all__'
    #success_url = reverse_lazy('past_detail')



class UpdatePhpView(LoginRequiredMixin,UpdateView):
    model = Php
    template_name = 'update_php.html'
    form_class = UpdatePhpForm

class UpdateBallView(LoginRequiredMixin,UpdateView):
    model = Easy_Ball
    template_name = 'edit_ball.html'
    fields = '__all__'
    #success_url = reverse_lazy('past_detail')


#update blog post
@superuser_required
def UpdatePostView(request, slug):
    # dictionary for initial data with
    # field names as keys



    # fetch the object related to passed id
    obj = get_object_or_404(Blog, slug = slug)

    # pass the object as instance in form
    form = UpdatePostForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        messages.info(request,"Post Added succesfully, Edit again?")

    detail = Blog.objects.filter(slug=slug)

    # add form dictionary to context
    context= {'form':form,'detail':detail}

    return render(request, "edit_post.html", context)

#update blog post
@superuser_required
def UpdateArticlePostView(request, slug):
    # dictionary for initial data with
    # field names as keys



    # fetch the object related to passed id
    obj = get_object_or_404(Article, slug = slug)

    # pass the object as instance in form
    form = UpdateArticlePostForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        messages.info(request,"Post Added succesfully, Edit again?")

    detail = Article.objects.filter(slug=slug)

    # add form dictionary to context
    context= {'form':form,'detail':detail}

    return render(request, "edit_blog.html", context)



@login_required
def UpdateSchoolPostView(request, slug):
    # dictionary for initial data with
    # field names as keys



    # fetch the object related to passed id
    obj = get_object_or_404(Brainy, slug = slug)

    # pass the object as instance in form
    form = UpdateSchoolPostForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        messages.info(request,"Post Added succesfully, Edit again?")

    brainhub = Blog.objects.filter(slug=slug)

    # add form dictionary to context
    context= {'form':form,'brainhub':brainhub}

    return render(request, "edit_school_post.html", context)

@login_required
def UpdateAcademic(request, slug):
    # dictionary for initial data with
    # field names as keys
    # fetch the object related to passed id
    obj = get_object_or_404(Academic, slug = slug)

    # pass the object as instance in form
    form = UpdateAcademicForm(request.POST or None, instance = obj)
    edu=Academic.objects.filter(slug=slug)
    if form.is_valid():
        form.save()
        messages.info(request,"Post Added succesfully, Edit again?")

    # add form dictionary to context
    context= {'form':form,'edu':edu}

    return render(request, "edit_academic.html", context)


@login_required
def StaffEditView(request,User):
    # dictionary for initial data with
    # field names as keys
    # fetch the object related to passed id
    obj = get_object_or_404(Profile, User = User)

    # pass the object as instance in form
    form = AuthorEditProfile(request.POST or None, instance = obj)
    user=Academic.objects.filter(User=User)
    if form.is_valid():
        form.save()
        messages.info(request,"Post Added succesfully, Edit again?")

    # add form dictionary to context
    context= {'form':form,'user':user}

    return render(request, "edit_author.html", context)





# create profile
class Staff_Profile_View(LoginRequiredMixin,CreateView):
    model= Profile
    template_name = 'create_profile.html'
    fields = ["bio","profile_pic","whatapp_url","facebook_url","google_url","linkeld_url",]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# add category
class AddCategoryView(LoginRequiredMixin,CreateView):
    model = Category
    template_name = 'addcategory.html'
    fields = '__all__'

# category list view
def category(request):
    cats=Category.objects.all()
    context={'cats':cats}
    return render(request,'category.html',context)

@admin_required
def requestpost(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request,'requestpost.html')
    else:
        form = UserArticleForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request,"Your post have been posted succesfully add another one ?")
        return render(request,'user_article_template.html',{'form':form})



def send_registration_email(user_email,username):
    context = {
        'username':username
    }
    subject = 'Welcome to benchatronics.com'
    html_message = render_to_string('user_email_reg.html',context)
    plain_message = strip_tags(html_message)
    from_email = 'noreply@benchatronics.com'
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    #triger the sending by calling this view any where you want it


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(username=username,password=password1)
            auth.login(request,user)
            user_email = user.email
            send_registration_email(user_email,username)
            messages.success(request,("You have successfully login"))
            return redirect('my_profile')
    else:
        form = SignUpForm
    return render(request, 'signup.html',{'form':form})


def privacy(request):
    return render(request,'privacy.html')



def terms(request):
    return render(request,'terms.html')



def handler404(request,exception):
    return render(request,'404.html')

def handler500(request):
    return render(request,'500.html')




# flutter detail view
def flutter_detail(request,slug):
    detail = Flutter.objects.filter(slug=slug).filter(draft=False)
    if detail.exists():
        detail = detail.first()
    else:
        raise http404
        #return HttpResponse("<h3>The Page you requested is been updated, Please check back later</h3>")

    post = Flutter.objects.filter(draft=False)
    posts = Flutter.objects.filter(draft=False).order_by('-updated')[:5]
    p = Paginator(post, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'detail':detail,'posts':posts,'page_obj':page_obj}
    return render(request,'flutter_detail.html', context)




def Detail_View(request,slug):
    posts = Blog.objects.filter(draft=False).order_by('-updated')[:10]
    news=Article.objects.filter(draft=False)[:10]
    detail = get_object_or_404(Blog, slug=slug)

    #search form
    form = SearchForm(request.GET or None)
    results = []

    context = {
        'form': form,'results': results,'posts':posts,'detail':detail,'news':news,
        'prev_post': detail.get_previous_item,
        'next_post': detail.get_next_item,}
    return render(request,'detail.html', context)


# question detail view
def Question_View(request,slug):
    if 'p' in request.GET:
        p = request.GET['p']
        #blog = Blog.objects.filter(blog_name__icontains=q)
        multiple_Q = Q(Q(title__icontains=p)|Q(content__icontains=p)|Q(date_added__icontains=p))

        question = Ask.objects.filter(multiple_Q)

    else:
        question = Ask.objects.filter(slug=slug)
    if question.exists():
        question = question.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'question':question,}
    return render(request,'ask_question.html', context)


def my_blog(request,slug):

    news=Article.objects.filter(draft=False)[:10]
    #detail = Article.objects.filter(slug=slug).filter(draft=False)
    detail = get_object_or_404(Article, slug=slug)

    form = SearchForm(request.GET or None)
    results = []

    context = {'form': form,'results': results,'detail':detail,'news':news,
        'prev_post': detail.get_previous_item,
        'next_post': detail.get_next_item,}
    return render(request,'my_blog.html', context)



def Javascript_View(request,slug):
    news=Article.objects.all()
    if 'p' in request.GET:
        p = request.GET['p']
        #blog = Blog.objects.filter(blog_name__icontains=q)
        multiple_Q = Q(Q(title__icontains=p)|Q(content__icontains=p)|Q(date_added__icontains=p))

        detail = Javascript.objects.filter(multiple_Q)

    else:

        detail = Javascript.objects.filter(slug=slug)
    if detail.exists():
        detail = detail.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'detail':detail,'news':news,}
    return render(request,'javascript.html', context)




# health detail view
def DetailHealthView(request,slug):
    posts=Blog.objects.all()
    tip=Health.objects.all()
    skul=Brainy.objects.all()
    tips = Health.objects.filter(slug=slug)

    if tips.exists():
        tips = tips.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'posts':posts,'tips':tips,'tip':tip,'skul':skul,}
    return render(request,'health_tips.html', context)



def categories(request,cate):
    categories_post = Blog.objects.filter(category=cate)
    if categories_post.exists():
        category = categories_post.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'categories_post':categories_post,'cate':cate.title(),}
    return render(request,'categories.html', context)


def category_health(request,categories):
    categories_health = Health.objects.filter(category=categories)
    if categories_health.exists():
        category = categories_health.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")

    context = {'categories_health':categories_health,'categories':categories.title(),}
    return render(request,'categories_health.html', context)

#mysql -u bechatronics -h bechatronics.mysql.pythonanywhere-services.com 'bechatronics$benny'  <  db-backupaddedflutterandkotlin.sql




#flutter list view
def flutter_list(request):
    posts=Flutter.objects.active()
    p = Paginator(posts, 20)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    return render(request, 'flutter_list.html', context)


def Blog_List(request):
    django = Blog.objects.all()
    p = Paginator(django, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)


    form = SearchForm(request.GET or None)
    results = []
    #search form
    context = {'form':form,'resuts':results, 'page_obj': page_obj}
    return render(request, 'blog.html', context)

def article(request):
    news=Article.objects.active()
    p = Paginator(news, 10)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    return render(request, 'article.html', context)

def Script_List(request):
    script=Javascript.objects.all()
    context = {'script':script,}
    return render(request, 'script_list.html', context)



#health  list view
def HealthPostView(request):

    tips=Health.objects.all()
    context = {'tips':tips,}
    return render(request, 'health.html', context)


class CategoryListView(ListView):
    model=Category
    template_name='category.html'


def logout(request):
    auth.logout(request)
    messages.info(request,'You have logged out successfully')
    response = redirect('/')
    #return redirect('/')
    response.delete_cookie('username')
    response.delete_cookie('login_status')
    return response


def schoolpost(request):
    tip=Health.objects.all()
    posts=Blog.objects.all()
    skul=Brainy.objects.all()
    context={'tip':tip,'posts':posts,'skul':skul}
    return render(request,'schoolpost.html',context)



def brainhub(request,slug):
    news = Article.objects.all()[:8]
    posts = Brainy.objects.all()[:20]
    brainhub = Brainy.objects.filter(slug=slug)
    form = SearchForm(request.GET or None)
    results = []


    if brainhub.exists():
        brainhub = brainhub.first()
    else:
        return HttpResponse("<h3>Page Not Found</h3>")



    context = {'form': form, 'results': results,
               'news':news,
               'prev_post': brainhub.get_previous_item,
               'next_post': brainhub.get_next_item,
               'brainhub':brainhub,'posts':posts,}
    return render(request,'brainhub.html', context)


def index(request):
   return render(request,'index.html')

#Ask question model used Brainy

@login_required(login_url='account_login')
def Ask_View(request):
    ask = Brainy.objects.all()
    context = {'ask':ask}
    return render(request,'question.html',context)

