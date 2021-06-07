from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from account.forms import PostEditForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView,UpdateView
from .models import Post, Home, Profile, Following
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,Http404, JsonResponse
from django.template.loader import render_to_string
from django.conf import settings

@login_required(login_url='/login')
def home(request):
    context = {}
    context ['posts'] = Post.objects.all().order_by('-pk')
    return render(request,'confess.html',context)

@login_required(login_url='/login')
def about(request):
    context = {}
    return render(request,'about.html',context)


def signup(request):
    if request.method=='POST':
        mail = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        conf_pass = request.POST.get('confirm_password', '')

        if User.objects.filter(username=username).exists():
            messages.success(request,'username is already taken')
            return redirect('/signup')
    
        if User.objects.filter(email=mail).exists():
            messages.success(request,'email is already taken')
            return redirect('/signup')

        if password != conf_pass:
            messages.success(request,'password is not matching')
        
        if len(password) <6:
            messages.success(request,'password is too short')

        Userchek = User.objects.filter(username=username) | User.objects.filter(email=mail)

        if password==conf_pass:
            user_obj = User.objects.create_user(password = password, email = mail, username = username)
            user_obj.save()
            messages.success(request, "your account has been created")
            return redirect("/login")
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        user_password = request.POST.get('password', '')
        user  = authenticate(username=user_name, password=user_password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "user or password is not matching")
    context = {}
    return render(request, 'index.html',context)

def user_logout(request):
    logout(request)
    return redirect("/login")

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    success_url='/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
   
    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        return False   

@login_required(login_url='/login')
def post_detail(request, id=id):
    postc = Post.objects.get(id=id)
    data = {
        'postc' : postc,   
    }        
    return render(request, 'post_detail.html', data) 


@login_required(login_url='/login')
def picpost(request):
 
    if request.method=='POST':
        image_ = request.FILES['image']
        user_ = request.user
        picpost_obj = Home(user = user_,  image=image_)
        picpost_obj.save()
        return redirect('/c/ph/')
  
@login_required(login_url='/login')
def pic_list(request):
    image = Home.objects.all().order_by('-id')
    return render(request, 'pic_list.html',  {'image':image})
       
@login_required(login_url='/login')
def pic_detail(request, id):
    post = Home.objects.get(id=id)
    is_liked =False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True  

    content = {
        'post' : post,
        'is_liked' : is_liked,
        'total_likes' : post.total_likes(),
    }
    return render(request, 'pic_detail.html', content)    

@login_required(login_url='/login')
def pro_detail(request, id):
    post = Home.objects.get(id=id)
    is_liked =False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True  

    content = {
        'post' : post,
        'is_liked' : is_liked,
        'total_likes' : post.total_likes(),
    }
    return render(request, 'pro_detail.html', content)    


def like_post(request):
    post = get_object_or_404(Home,id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post' :post,
        'is_liked' :is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('account/like_section.html', context, request=request)
        return JsonResponse({'form':html})

@login_required(login_url='/login')
def PostCreateView(request):
 
    if request.method=='POST':
        image_ = request.FILES['conimage']
        description_ = request.POST.get('content','')
        user_ = request.user
        picpost_obj = Post(user = user_, content=description_,  conimage=image_)
        picpost_obj.save()
        return redirect('/')
 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url ='/'

    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        return False            

class PicDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Home
    success_url = '/c/ph/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

@login_required(login_url='/login')
def userProfile(request, username):
    user = User.objects.filter(username=username)
    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        post = getPost(user)
        bio = profile.bio
        user_img = profile.userImage
        
        is_following = Following.objects.filter(user = request.user, followed = user)
        following_obj = get_object_or_404(Following ,user = user)
        follower, following = following_obj.follower.count(), following_obj.followed.count()

        data = {
            'user_obj':user,
            'bio':bio,
            'follower':follower,
            'following':following,
            'userImg':user_img,
            'posts':post,
            'connection':is_following
        }
    else: return HttpResponse("NO SUCH USER")

    return render(request, 'profile.html', data)
    
    
def getPost(user):
    post_obj = Home.objects.filter(user=user)
    imgList= [post_obj[i:i+3] for i in range(0, len(post_obj), 3)]
    return imgList

def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username = username)

    #check if already following
    following = Following.objects.filter(user = main_user, followed = to_follow)
    is_following = True if following else False

    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True

    resp = {
        "following" : is_following,
    }

    return HttpResponseRedirect(reverse('user_profile',args=[username]))

class Search_User(ListView):
    model = Profile
    template_name = "search.html"
    context_object_name = 'account'

    def get_queryset(self):
        user = self.request.GET.get("username","")
        queryset = Profile.objects.filter(user__username__icontains = user)
        return queryset

class ProfileListView(ListView):
    model = Profile
    template_name = 'main.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Profile.objects.all().order_by('-id').exclude(user=self.request.user)

class userEdit(UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    fields = ['bio', 'userImage']
    success_url = '/'

class userSetting(UpdateView):
    model = User
    template_name = 'setting.html'
    fields = ['username', 'email']
    success_url = '/'

