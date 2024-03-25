from .models import *
from django import forms
#from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm,UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.conf import settings
from django.core.mail import send_mail
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.core.exceptions import ValidationError
from django.db import IntegrityError
#########################




class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100)


# contact/forms.py
class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)
    #attach = forms.FileField(label="Please select at least one file",required=False,widget=forms.ClearableFileInput(attrs={'multiple': True}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,label="Enter your first name",widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={ 'class':'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','captcha')

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class EditProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your email to submit', 'class':'form-control'}))
    #is_active = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    #is_superuser = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    #is_staff = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    #last_login = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    #date_joined = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-check'}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',)#'is_active',)#'password')


class AuthorEditProfile(UserChangeForm):
    user = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    bio = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    google_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    linked_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    google_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = '__all__'

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2',)


#choices=[('Coding','Coding'),('Hacking','Hacking'),('News','News')]
"""choices = Category.objects.all().values_list('name','name')
choice_list =[]
for item in choices:
    choice_list.append(item)
"""
class HealthPostForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = '__all__'
        widgets = {
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

class AcademicForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Academic
        fields = '__all__'
        widgets = {
            'tag':forms.TextInput(attrs={'class':'form-control','placeholder':'E.g chainrule,product rule',}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'semester_course': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }



class PyForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Python
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'last_updated': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),

        }


class PhpForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Php
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'last_updated': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),

        }





class Update_Flutter(forms.ModelForm):
    class Meta:
        model = Flutter
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'id':'form_warning','class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }




class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            'title': forms.TextInput(attrs={'id':'form_warning','class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }



class UpdatePhpForm(forms.ModelForm):
    class Meta:
        model = Php
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

class UpdatePythonForm(forms.ModelForm):
    class Meta:
        model = Python
        fields = '__all__'

        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            'title': forms.TextInput(attrs={'id':'form_warning', 'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'last_updated': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),

        }


class UpdateAcademicForm(forms.ModelForm):
    class Meta:
        model = Academic
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'table_of_content': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }



class UpdateSchoolPostForm(forms.ModelForm):
    class Meta:
        model = Brainy
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'publish': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }




#update health post
class UpdateHealthPostForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = '__all__'
        widgets = {
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

class UpdateBallForm(forms.ModelForm):
    class Meta:
        model = Easy_Ball
        fields = '__all__'
        widgets = {
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

#blog post
class SchoolPostForm(forms.ModelForm):
    class Meta:
        model = Brainy
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'publish': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }


#blog post
class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'summer_content': SummernoteWidget(),
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'id':'form_warning','class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }
        



#flutter post
class FlutterForm(forms.ModelForm):
    class Meta:
        model = Flutter
        fields = '__all__'
        widgets = {
            'tags': SummernoteWidget(),
            'title': forms.TextInput(attrs={'id':'form_warning','class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            #'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            slug = self.cleaned_data.get('slug')
            if Flutter.objects.filter(slug=slug).exists():
                self.ValidatetionError('This topic with this content already exists.')
                return slug





class BallForm(forms.ModelForm):
    class Meta:
        model = Easy_Ball
        fields = '__all__'
        widgets = {
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }




class UserArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body','tag','author',)
        widgets = {
            #'body': forms.TextInput(required=True,attrs={'class':'form-control',}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }







class AdminArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tags': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
        }




class UpdateArticlePostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            # 'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.TextInput(attrs={'class':'form-control',}),
            'content': forms.TextInput(attrs={'class':'form-control'}),
            'keyword': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'date_added': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'value':'','class':'form-control','id':'user_author','type':'hidden'}),
        }

