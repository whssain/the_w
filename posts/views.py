from django.shortcuts import render , redirect
from .models import *
from django.shortcuts import get_object_or_404
from .forms import PostForm ,UserSignUp ,UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404 , JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate,login ,logout
# Create your views here.
"""def post_create(request):
	post_list = Post.objects.all()
	post_filter = Post.objects.filter(title='Noor')
	post_get = Post.objects.get(title = "gf")
	context={
	"user": request.user,
	"list": post_list,
	"filter": post_filter,
	get": post_get

	#"random_number":random.re
	
	}
	 return render(request,'create.html',context) """

def like_button(request,post_id):
	obj=Post.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user , post=obj)

	if created:
		action="like"
	else:
		action="unlike"
		like.delete()
	post_like_count = obj.like_set.all().count()


	context ={

		"action":action,
		"like_count":post_like_count,

	}


	return JsonResponse(context, safe=False)
def usersignup(request):
	context ={}
	form = UserSignUp()
	context['form']=form
	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():

			user = form.save(commit=False)
			username = user.username
			password = user.password
			user.set_password(password)
			user.save()
			auth_user = authenticate(username=username,password=password)
			login(request,auth_user)
			

			return redirect("posts:list")
		messages.error(request,form.errors)
		return redirect("posts:signup")
	return render(request,'signup.html', context)

def post_detail(request ,slug):
	obj=get_object_or_404(Post, slug=slug)
	date =timezone.now().date()

	if obj.publish > date or obj.draft:
		if not request.user.is_staff or request.user.is_superuser:
			raise Http404
	if request.user.is_authenticated():
		if Like.objects.filter(post=obj,user=request.user).exists():
			like=True 
		else :
			like = False
	post_like_count = obj.like_set.all().count()

	user_like_count = request.user.like_set.all().count()
	context ={
	"object":obj,
	}
	return render(request,'post_detail.html',context)
def user_login(request):

	context ={}
	form = UserLogin()
	context['form']=form
	if request.method == "POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']

			auth_user = authenticate(username=username,password=password)
			login(request,auth_user)
			return redirect("posts:list")
			messages.error(request,"Wrong username/password combination. Please try again.")
			print ("--------------")
			print(author_user)
			print ("--------------")
			return redirect("posts:login")
			messages.error(request,form.errors)
			return redirect("posts:login")

		
	return render(request,'login.html', context)

def userlogout(request):
	logout(request)
	return redirect("posts:login")

def post_list(request):
	today = timezone.now().date()

	if request.user.is_staff or request.user.is_superuser:
		obj_list = Post.objects.all()
	else:
		obj_list = Post.objects.filter(draft=False).filter(publish__lte=today)


	query = request.GET.get("q")
	if query:
		obj_list=obj_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

	paginator = Paginator(obj_list, 4) # Show 5 contacts per page
	page = request.GET.get('page')
	try:
		obj = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		obj = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		obj = paginator.page(paginator.num_pages)
	context = {
	"post_list": obj,
	
	"today": today,
	}
	return render(request, 'post_list.html', context)
def post_create(request):

	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		obj =form.save(commit=False)
		obj.author = request.user
		obj.save()
		messages.success(request,"OMG! So Cool!")
		return redirect ("posts:list")
	context = {
		"form":form
	}
	return render(request,'post_create.html',context)


def post_update(request,slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	post_object = get_object_or_404(Post , slug=slug)
	form = PostForm(request.POST or None , request.FILES or None ,instance=post_object)
	if form.is_valid():
		form.save()
		#messages.success(request,"Giving it a second thought?")
		return redirect ("posts:list")
	context = {
		"form":form,
		"post_object":post_object,
	}
	return render(request,'post_update.html',context)

def post_delete(request, slug):
	if not (request.user.is_superuser):
		raise Http404
	Post.objects.get(slug=slug).delete()
	messages.warning(request ,"Seriously bro?")
	return redirect ("posts:list")
	
