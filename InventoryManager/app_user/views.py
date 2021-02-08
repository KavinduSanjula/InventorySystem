from django.shortcuts import render, redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				request.session['user'] = user.id
				return redirect('/')

		else:
			return HttpResponse('Invalid login details')

	else:
		return render(request,'app_user/login.html')

@login_required
def special(request):
	return HttpResponse('user page')

@login_required
def user_logout(request):
	request.session.pop('user')
	logout(request)
	return redirect('/')
