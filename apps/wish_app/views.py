from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User
from .models import Item

def flash_errors(errors, request):
	for error in errors:
		messages.error(request, error)

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def user(request, id):
	context={
		'user': current_user(request),
	}
	return render(request, 'wish_app/index.html')

def index(request):
	return render(request, 'wish_app/index.html')

def register(request):
	if request.method =="POST":
		errors = User.objects.validate_registration(request.POST)

		if not errors:
			user = User.objects.create_user(request.POST)
			request.session['user_id'] = user.id
			return redirect(reverse('dashboard'))

		flash_errors(errors, request)
	return redirect(reverse('landing'))

def login(request):
	if request.method == "POST":
		check = User.objects.validate_login(request.POST)

		if 'user' in check:
			request.session['user_id'] = check['user'].id

			return redirect(reverse('dashboard'))

		flash_errors(check['errors'], request)
	return redirect(reverse('landing'))

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect(reverse('landing'))

def dashboard(request):
	if 'user_id' not in request.session:
		return redirect('/')

	user = current_user(request)
	context = {
		'user': user, 
		'notwished': Item.objects.exclude(wished_by = user),
	}
	return render(request, 'wish_app/dashboard.html', context)

def show_item(request, item_id):
	item = Item.objects.get(id = item_id)
	context = {
		'item': item,
		'users': item.wished_by.all()
	}
	return render(request, 'wish_app/item.html', context)

def create(request):
	if request.method == "POST":
		errors = Item.objects.validate(request.POST)

		if not errors:
			item = Item.objects.create_item(request.POST, request.session["user_id"])
			return redirect(reverse('add_wish', args = (item.id, )))

		flash_errors(request, errors)
		return redirect(reverse('create_item'))
	else:
		return render(request, 'wish_app/create.html')

def add_wish(request,item_id):
	Item.objects.add_wish(item_id, request.session["user_id"])
	return redirect(reverse('dashboard'))

def remove_wish(request,item_id):
	Item.objects.remove_wish(item_id, request.session["user_id"])
	return redirect(reverse('dashboard'))

def delete(request, item_id):
	Item.objects.delete_item(item_id)
	return redirect(reverse('dashboard'))