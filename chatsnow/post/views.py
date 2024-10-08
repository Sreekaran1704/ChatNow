from django.shortcuts import render
from .models import Post
from .forms import PostForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')

def post_list(request):
    Posts = Post.objects.all().order_by('-created')
    return render(request,'post_list.html', {'Posts': Posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.user = request.user
            Post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    
    return render(request,'post_form.html', {'form': form})

@login_required
def post_update(request,post_id):
    post = get_object_or_404(Post , pk = post_id , user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid() :
            return redirect('post_list')
    else:
        form = PostForm(instance = post)
    
    return render(request,'post_form.html', {'form': form})

@login_required
def post_delete(request,post_id):
    post = get_object_or_404(Post , pk = post_id , user = request.user)
    if request.method == 'POST' :
        post.delete()
        return redirect('post_list')
    
    return render(request,'post_confirm_delete.html',{'post':post})


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('post_list')

    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})


def search_users(request):
    query = request.GET.get('search_data') or request.POST.get('search_data')
    posts = []
    if query:
        posts = Post.objects.filter(
            Q(user__username__icontains=query) |
            Q(text__icontains=query)
        ).select_related('user')
    
    context = {
        'query': query,
        'posts': posts,
    }
    return render(request, 'search.html', context)
