from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validate_registration(self, form_data):
		errors =[]
		name = form_data['name']
		user_name = form_data['user_name']
		password = form_data['password']
		confirmation_password = form_data['password_confirmation']

		if len(name) == 0:
			errors.append("Name is required!")

		if len(user_name) == 0:
			errors.append("User Name is required!")

		if len(name) < 3:
			errors.append("Name must be more than 3 characters!")

		if len(user_name) < 3:
			errors.append("User Name must be more than 3 characters!")
		
		if len(password) == 0:
			errors.append("Password is required!")
		if len(password) < 8:
			errors.append("Password must be > 8 characters long!")
		elif password != confirmation_password:
			errors.append("Passwords must match!")

		return errors

	def validate_login(self, form_data):
		errors = []
		user_name = form_data['user_name']
		password = form_data['password']
		
		if len(user_name) == 0:
			errors.append("User Name is required!")
		
		if len(password) == 0:
			errors.append("Password is required!")

		if not errors:
			user_list = User.objects.filter(user_name=user_name)

			if user_list:
				user = user_list[0]
				user_password = password.encode()
				db_password = user.password.encode()

				if bcrypt.checkpw(user_password, db_password):
					return {'user': user}

		errors.append("User Name or Password Invalid!")

		return {'errors': errors}

	def create_user(self, form_data):
		password = form_data['password']
		hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		return User.objects.create(
			name = form_data['name'],
			user_name = form_data['user_name'],
			password = hashedpw,
		)

class User(models.Model):
	name = models.CharField(max_length=45)
	user_name = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __unicode__(self):
		return "id: {}, name: {}, user_name: {}, password: {}".format(self.id, self.name, self.user_name, self.password)

class ItemManager(models.Manager):
	def validate(self, form_data):
		errors = []
		name = form_data['name']

		if len(name) == 0:
			errors.append("Please type name of item!")
		if len(name) < 3:
			errors.append("Item name should be more than 3 characters long!")

		return errors

	def add_wish(self, item_id, user_id):
		user = User.objects.get(id= user_id)
		item = Item.objects.get(id= item_id)
		user.wishes.add(item)

	def remove_wish(self, item_id, user_id):
		user = User.objects.get(id= user_id)
		item = Item.objects.get(id= item_id)
		user.wishes.remove(item)

	def create_item(self, form_data, user_id):
		user = User.objects.get(id=user_id)
		wish = self.create(
		name = form_data['name'],
		added_by = user
		)
		return wish

	def delete_item(self, item_id):
		item = Item.objects.get(id= item_id).delete()

class Item(models.Model):
	name = models.CharField(max_length=150)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	added_by = models.ForeignKey(User, related_name="added_items")
	wished_by = models.ManyToManyField(User, related_name="wishes")
	objects = ItemManager()

	def __unicode__(self):
		return "id: {}, name: {}, added_by: {}, wished_by: {}".format(self.id, self.name, self.added_by, self.wished_by)
