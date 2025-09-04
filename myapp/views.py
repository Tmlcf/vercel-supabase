
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
	return render(request, 'index.html')

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect('/home/')
		else:
			return render(request, 'index.html', {'login_error': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'})
	return redirect('/')

# เพิ่ม view สำหรับ home
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def home_view(request):
	return render(request, 'home.html')

@csrf_protect
def register_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		if User.objects.filter(username=username).exists():
			return render(request, 'index.html', {'register_error': 'ชื่อผู้ใช้นี้มีอยู่แล้ว'})
		if User.objects.filter(email=email).exists():
			return render(request, 'index.html', {'register_error': 'อีเมลนี้มีอยู่แล้ว'})
		user = User.objects.create_user(username=username, email=email, password=password)
		user.save()
		return render(request, 'index.html', {'register_success': 'สมัครสมาชิกสำเร็จ! สามารถล็อกอินได้เลย'})
	return redirect('/')
