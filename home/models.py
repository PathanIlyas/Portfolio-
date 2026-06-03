from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    name = models.CharField(default='Your Name', max_length=100)
    title = models.CharField(default='Full Stack Developer', max_length=150)
    tagline = models.CharField(default='Clean UI | Robust Backend', max_length=200)
    bio = models.TextField(default='I build scalable, high-performance web applications.')
    email = models.EmailField(default='your@email.com')
    github = models.URLField(blank=True, default='https://github.com')
    linkedin = models.URLField(blank=True, default='https://linkedin.com')
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile/')
    resume = models.FileField(blank=True, null=True, upload_to='resume/')
    available = models.BooleanField(default=True)
    years_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    clients_served = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('devops', 'DevOps & Tools'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, default='backend', max_length=20)
    percentage = models.PositiveIntegerField(default=80, help_text='Skill level 0-100')
    icon_class = models.CharField(blank=True, help_text='FontAwesome class e.g. fa-brands fa-python', max_length=100)
    color = models.CharField(blank=True, default='#00f3ff', max_length=20)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    featured = models.BooleanField(default=False)
    github_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    tags = models.CharField(blank=True, max_length=200, help_text='Comma-separated tags e.g. Django,Python,API')

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    project_type = models.CharField(blank=True, max_length=100)
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='new', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'
