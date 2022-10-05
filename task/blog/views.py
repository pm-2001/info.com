
from ast import Subscript
from audioop import reverse
from xml.etree.ElementTree import Comment
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from datetime import datetime
from blog.models import Category, Post,Comment,Contact,Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from .forms import ImageForm,CommentForm,CreateUserForm,EditProfileForm,PasswordChangingForm,ProfileForm
from django.views.generic import DetailView,UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from django.contrib.auth.views import PasswordChangeView


def home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    return render(request,'index.html',{'posts':posts,'categories':categories})

def LikeView(request, pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('postdetail' , args=[str(pk)]))

def CategoryView(request,cats):
    category_posts=Post.objects.filter(category=cats)
    return render(request,'categories.html',{'cats':cats,'category_posts':category_posts})

class PostDetail(DetailView):
    model = Post
    template_name = 'postdetail.html'

    def get_context_data(self,*args,**kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        posts = Post.objects.all()
        stuff=get_object_or_404(Post, id=pk)
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id = self.request.user.id).exists():
            liked=True
        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()

        context['post'] = post
        context['posts'] = posts
        context['comments'] = comments
        context['form'] = form
        context["total_likes"] = total_likes
        context[" liked "] = liked
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super(PostDetail, self).get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comments.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            body = form.cleaned_data['body']

            comment = Comment.objects.create(name=name, body=body, post=post)

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)


class UpdatePostView(UpdateView):
    model= Post
    template_name = 'update_post.html'
    fields = ['title','body','image','snippet']
    success_url= reverse_lazy('myblogs')

class DeletePostView(DeleteView):
    model= Post
    template_name = 'delete_post.html'
    success_url= reverse_lazy('myblogs')

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

def about(request):
    return render(request,'about.html')

def profile(request,pk):
    user_form = EditProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="profile.html",context={"user":request.user, "user_form":user_form, "profile_form":profile_form,})

def editprofile(request):
    if request.method == "POST":
        user_form = EditProfileForm(request.POST,request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() or profile_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))
            print (User.pk)
            return render (request,'profile.html')
            # return redirect ('profile/pk')
        # elif profile_form.is_valid():
        #     profile_form.save()
        #     messages.success(request,('Your profile was successfully updated!'))
        #     return redirect ('profile')
        else:
            messages.error(request,('Unable to complete request'))
            return render (request,'edit_profile.html')
    user_form = EditProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="edit_profile.html", context={"user":request.user, "user_form":user_form, "profile_form":profile_form })
    
@login_required(login_url='signin')
def posts(request):
    user=request.user
    form = ImageForm(initial={'username':user})
    if request.method == "POST":
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save() 
            messages.success(request,'Post created successfully')
            return redirect("myblogs")
        else:
            messages.success(request,'Invalid Post') 
    context = {'form':form}
    return render(request,'posts.html',context)

@login_required(login_url='signin')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone = phone, desc=desc,date = datetime.today())
        contact.save()
        messages.success(request,'Submitted successfully')
    return render(request,'contact.html')

def register(request):
    form = CreateUserForm() 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created successfully')
            return redirect('signin')
        else:
            messages.success(request,"password didn't match!")
            return render(request,'register.html')
    context = {'form':form}
    return render(request,'register.html',context)

def password_success(request):
    profiles = Profile.objects.all()
    return render(request,'password_success.html',{'profiles':profiles})

class PasswordsChangeView(PasswordChangeView):
    form_class=PasswordChangingForm
    success_url = reverse_lazy('password_success')

    def get(self, request):
        profiles = Profile.objects.all()
        return render(request,'change_password.html',{'profiles':profiles})

def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.success(request,'Username or password is incorrect!')
            return render(request,'signin.html')
    return render(request,'signin.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

@login_required(login_url='signin')
def myblogs(request):
    user=request.user
    posts = user.post_set.filter(username=user)
    return render(request,'myblogs.html',{'posts':posts})


# class AddCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name= 'postdetail.html'
#     # fields= '__all__'
#     def form_valid(self,form):
#         form.instance.post_id = self.kwargs['pk']
#         return super().form_valid(form)
#     success_url= reverse_lazy('home') 
