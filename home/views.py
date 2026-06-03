from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, CustomUser, Profile, Skill, ContactMessage
from .forms import EmailAuthenticationForm, ProjectForm, ClientRegistrationForm, SkillForm, ProfileForm

def get_profile():
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(
            name="Ilyas Khan",
            title="Full Stack Developer",
            tagline="Clean UI | Robust Backend",
            bio="I build scalable, high-performance web applications using advanced architectures. Specializing in Django, Python, and modern frontend systems.",
            email="ilyaskhanik1325@gmail.com",
            github="https://github.com/PathanIlyas",
            linkedin="https://www.linkedin.com/in/ilyas-khan-192876292/",
            available=True,
            years_experience=3,
            projects_completed=20,
            clients_served=10
        )
    return profile

# Public Views
def index(request):
    profile = get_profile()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        project_type = request.POST.get('project_type', '')
        message = request.POST.get('message')
        
        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            project_type=project_type,
            message=message
        )
        
        try:
            # 1. Send email to Admin
            send_mail(
                f"New Contact Form Submission from {name}",
                f"Client Email: {email}\nProject Type: {project_type}\n\nMessage:\n{message}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER], # Admin's email
                fail_silently=False,
            )
            
            # 2. Send confirmation to Client
            send_mail(
                "Thank you for contacting me!",
                f"Hi {name},\n\nI have received your message and will get back to you shortly.\n\nYour message:\n{message}",
                settings.EMAIL_HOST_USER,
                [email], # Client's email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully! Check your email for confirmation.")
        except Exception as e:
            messages.error(request, f"Error sending email. Please check SMTP configuration. ({str(e)})")
            
        return redirect('index')
        
    return render(request, "home/index.html", {
        "projects": projects,
        "profile": profile,
        "skills": skills
    })

def about_view(request):
    profile = get_profile()
    return render(request, "home/about.html", {"profile": profile})

def expertise_view(request):
    profile = get_profile()
    skills = Skill.objects.all()
    return render(request, "home/expertise.html", {"profile": profile, "skills": skills})

def projects_view(request):
    profile = get_profile()
    projects = Project.objects.all()
    return render(request, "home/projects.html", {"profile": profile, "projects": projects})

def contact_view(request):
    profile = get_profile()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        project_type = request.POST.get('project_type', '')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            project_type=project_type,
            message=message
        )
        
        try:
            send_mail(
                f"New Contact Form Submission from {name}",
                f"Client Email: {email}\nProject Type: {project_type}\n\nMessage:\n{message}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
            )
            send_mail(
                "Thank you for contacting me!",
                f"Hi {name},\n\nI have received your message and will get back to you shortly.\n\nYour message:\n{message}",
                settings.EMAIL_HOST_USER,
                [email],
            )
            messages.success(request, "Your message has been sent successfully! Check your email for confirmation.")
        except Exception as e:
            messages.error(request, f"Error sending email. Please check SMTP configuration. ({str(e)})")
            
        return redirect('contact')
        
    return render(request, "home/contact.html", {"profile": profile})

# Client Authentication Views
def client_register(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False # Ensure it's a client
            user.save()
            login(request, user)
            messages.success(request, "Registration successful! You can now send a message.")
            return redirect('index')
    else:
        form = ClientRegistrationForm()
    return render(request, 'home/client_register.html', {'form': form})

def client_login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.email}!")
            if user.is_staff:
                return redirect('dashboard')
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'home/client_login.html', {'form': form})

# Admin Authentication Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:
                messages.error(request, "You do not have admin access.")
                return redirect('client_login')
                
            login(request, user)
            messages.success(request, f"Welcome Admin, {user.email}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()
        
    return render(request, 'home/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

# Custom Admin Dashboard Views
def get_dashboard_context(extra_context=None):
    context = {
        'new_messages': ContactMessage.objects.filter(status='new').count()
    }
    if extra_context:
        context.update(extra_context)
    return context

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        return redirect('index')
    projects = Project.objects.all()
    skills_count = Skill.objects.count()
    profile = get_profile()
    context = get_dashboard_context({
        'projects': projects,
        'skills_count': skills_count,
        'profile': profile
    })
    return render(request, 'home/dashboard.html', context)

@login_required(login_url='login')
def project_add(request):
    if not request.user.is_staff: return redirect('index')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully.")
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    context = get_dashboard_context({
        'form': form,
        'action': 'Add'
    })
    return render(request, 'home/project_form.html', context)

@login_required(login_url='login')
def project_edit(request, pk):
    if not request.user.is_staff: return redirect('index')
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
        
    context = get_dashboard_context({
        'form': form,
        'action': 'Edit'
    })
    return render(request, 'home/project_form.html', context)

@login_required(login_url='login')
def project_delete(request, pk):
    if not request.user.is_staff: return redirect('index')
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('dashboard')
        
    context = get_dashboard_context({
        'project': project
    })
    return render(request, 'home/project_confirm_delete.html', context)

# Dashboard - Skills CRUD Views
@login_required(login_url='login')
def skill_list(request):
    if not request.user.is_staff: return redirect('index')
    skills = Skill.objects.all()
    context = get_dashboard_context({'skills': skills})
    return render(request, 'home/skill_list.html', context)

@login_required(login_url='login')
def skill_add(request):
    if not request.user.is_staff: return redirect('index')
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully.")
            return redirect('skill_list')
    else:
        form = SkillForm()
    
    context = get_dashboard_context({
        'form': form,
        'action': 'Add'
    })
    return render(request, 'home/skill_form.html', context)

@login_required(login_url='login')
def skill_edit(request, pk):
    if not request.user.is_staff: return redirect('index')
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully.")
            return redirect('skill_list')
    else:
        form = SkillForm(instance=skill)
        
    context = get_dashboard_context({
        'form': form,
        'action': 'Edit'
    })
    return render(request, 'home/skill_form.html', context)

@login_required(login_url='login')
def skill_delete(request, pk):
    if not request.user.is_staff: return redirect('index')
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully.")
        return redirect('skill_list')
        
    context = get_dashboard_context({
        'skill': skill
    })
    return render(request, 'home/skill_confirm_delete.html', context)

# Dashboard - Profile View/Edit
@login_required(login_url='login')
def profile_edit(request):
    if not request.user.is_staff: return redirect('index')
    profile = get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
        
    context = get_dashboard_context({
        'form': form
    })
    return render(request, 'home/profile_form.html', context)

# Dashboard - Messages Inbox
@login_required(login_url='login')
def message_list(request):
    if not request.user.is_staff: return redirect('index')
    inbox_messages = ContactMessage.objects.all()
    context = get_dashboard_context({'inbox_messages': inbox_messages})
    return render(request, 'home/message_list.html', context)

@login_required(login_url='login')
def message_detail(request, pk):
    if not request.user.is_staff: return redirect('index')
    msg = get_object_or_404(ContactMessage, pk=pk)
    if msg.status == 'new':
        msg.status = 'read'
        msg.save()
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(ContactMessage.STATUS_CHOICES):
            msg.status = status
            msg.save()
            messages.success(request, f"Message status updated to {msg.get_status_display()}.")
            return redirect('message_list')
            
    context = get_dashboard_context({
        'msg': msg
    })
    return render(request, 'home/message_detail.html', context)

@login_required(login_url='login')
def message_delete(request, pk):
    if not request.user.is_staff: return redirect('index')
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('message_list')
        
    context = get_dashboard_context({
        'msg': msg
    })
    return render(request, 'home/message_confirm_delete.html', context)
