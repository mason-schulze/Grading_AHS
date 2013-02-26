from django.db import models
from django import forms
from django.contrib.auth.models import User

# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )


# class MyUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=MyUserManager.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class MyUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#         db_index=True,
#     )
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     objects = MyUserManager()

#     def get_full_name(self):
#         return self.first_name + " " + self.last_name

#     def get_short_name(self):
#         # The user is identified by their email address
#         return (self.first_name[0] + self.last_name).lower()

#     def __unicode__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin


class StudentCreationForm(forms.ModelForm):
    username = models.CharField(max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(StudentCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = False
        if commit:
            user.save()
        return user


class TeacherCreationForm(forms.ModelForm):
    username = models.CharField(max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(TeacherCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user
