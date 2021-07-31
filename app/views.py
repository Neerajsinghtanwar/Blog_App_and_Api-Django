from django.contrib.auth.models import Group, User, Permission
from django.core import paginator
from app.models import Blog, Contact
from app.forms import BlogForm, Loginform, Signupform, UserDetail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from app.middlewares import underconstructionmiddleware
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    a = request.user.groups.all()
    print("~~~~~~~~~~~~~~~~~~~~~~~~",a)
    blog = Blog.objects.all().order_by('id')
    paginator = Paginator(blog, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'app/home.html', {'blogs':page_obj})

@underconstructionmiddleware
def about(request):
    pass

def contact(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email_id")
        phone = request.POST.get("phone_no.")
        desc = request.POST.get("desc")
        if fname != '' and lname != '' and email != '' and phone != '':
            details = Contact(fname=fname, lname=lname, email=email, phone=phone, desc=desc )
            details.save()
            messages.success(request, "We will contact you soon!!")
        else:
            messages.error(request, "Field are empty!!")
    return render(request, 'app/contact.html')

@login_required
def dashboard(request):
    if request.user.is_staff:
            blog = Blog.objects.all().order_by('id')
            paginator = Paginator(blog, 2)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
    else:
        blog = Blog.objects.filter(creator=request.user).all().order_by('id')
        paginator = Paginator(blog, 2)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

    user = request.user
    group = request.user.groups.all()
    ip = request.session.get('ip',0)
    full_name = user.get_full_name()
    login_count = cache.get('count', version=user.pk)
        
    return render(request, 'app/dashboard.html', {'blogs':page_obj, 'groups':group, 'ip':ip, 'fullname':full_name, 'ct':login_count})

def signup(request):
    if request.method == 'POST':
        fm = Signupform(request.POST)
        if fm.is_valid():
            user = fm.save()
            group = Group.objects.get_or_create(name='Blogger')
            user.groups.add(group)

            messages.success(request, "Your accout is created successfully!!")
        else:
            messages.warning(request, "Please fill all the details!!")
    else:
        fm = Signupform()
    return render(request, 'app/signup.html', {'form':fm})


def add_staff(request):
    if request.method == 'POST':
        fm = Signupform(request.POST)
        if fm.is_valid():
            user = User.objects.create(username=fm.data['username'], first_name=fm.data['first_name'], last_name=fm.data['last_name'], email=fm.data['email'], password=fm.data['password1'], is_staff=True)
            perm = Permission.objects.get(name='Can delete blog')
            user.user_permissions.add(perm)
            user.save()
            messages.success(request, "Your accout is created successfully!!")
            
        else:
            messages.warning(request, "Please fill all the details!!")
    else:
        fm = Signupform()
    return render(request, 'app/signup.html', {'form':fm})


def user_login(request):
    if request.method == 'POST':
        fm = Loginform(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
    else:
        fm = Loginform()
    return render(request, 'app/login.html', {'form':fm})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def edit_blog(request, pk, slug):
    blog = Blog.objects.get(id=pk, slug=slug)
    if request.method == 'POST':        
        fm = BlogForm(request.POST, instance=blog)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Blog updated successfully!!")
    else:
        fm = BlogForm(instance=blog)
    return render(request, 'app/editblog.html', {'form':fm, 'id':pk, 'slug':"slug"})


@login_required
def delete_blog(request, pk, slug):
    blog = Blog.objects.get(id=pk, slug=slug)
    blog.delete()
    messages.success(request, "Blog deleted successfully!!")
    return HttpResponseRedirect('/dashboard/')


@login_required
def create_blog(request):    
    if request.method == 'POST':
        fm = BlogForm(request.POST)
        if fm.is_valid():
            title = fm.cleaned_data['title']
            desc = fm.cleaned_data['desc']
            details = Blog(title=title, desc=desc, creator=request.user)
            details.save()
            messages.success(request, "Blog created successfully!!")
    else:
        fm = BlogForm()
    return render(request, 'app/createblog.html', {'form':fm})


@login_required
@underconstructionmiddleware
def useraccount(request):
    return render(request, 'app/useraccount.html')


def userprofile(request):
    fm = UserDetail(instance=request.user)
    return render(request, 'app/userprofile.html', {'form':fm})


def edituserprofile(request):
    if request.method == 'POST':
        fm = UserDetail(request.POST, instance=request.user)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Profile edit successfully!!")
    else:
        fm = UserDetail(instance=request.user)
    return render(request, 'app/edituserprofile.html', {'form':fm})