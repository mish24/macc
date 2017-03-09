from signup.models import Pcuser
from django.contrib.auth.models import User
from uuid import uuid4

import random, decimal
from random import randint


MAIL_PROVIDERS = ("@yahoo.com", "gmail.com", "@outlook.com", "riseup.net", "rediffmail.com", "anything.com")
MAIL_IDS = ("name1", "name2", "name3", "name4", "name5", "name6", "name7", "name8", "name9", "name10")
NAMES_LIST = ("name1", "name2", "name3", "name4", "name5", "name6", "name7")

LOCATION_LIST = ("Location place 1", "Location place 2", "Location place 3", "Location place 4", "Location place 5")
GENDER_LIST = ("Male", "Female")


def create_random_admin():


	user_1 = User.objects.create_user(
		username = random.choice(NAMES_LIST).lower().strip() + uuid4().hex[:9],
		email = random.choice(MAIL_IDS).lower().strip() + random.choice(MAIL_PROVIDERS),
		password = 'correct_password'
		)
	user_1.save()

	return user_1




def create_random_pcuser():

	"""the admin cannot login directly to the site
	he/she must be registered as a Pcuser (form the admin page) to do so
	This function can also be called any number of times for testing purpose
	"""

	user = User.objects.create_user(
		username = random.choice(NAMES_LIST).lower().strip() + uuid4().hex[:9],
		email = random.choice(MAIL_IDS).lower().strip() + random.choice(MAIL_PROVIDERS),
		password = 'correct_password'
		)

	pcuser = Pcuser.objects.create(
		user = user,
		location = random.choice(LOCATION_LIST),
		phone = randint(100000000, 9999999999),
		gender = random.choice(GENDER_LIST),
		reset_pass = '1',
		verified = '1'
		)
	pcuser.save()

	return pcuser

#functions with hard coded data to personally look up 

def create_known_admin():

	"""This creates an admin with hard coded data which
	is already known to us. But this can be used only once
	Calling this again gives error
	"""

	user = User.objects.create_user(
		username = 'tester',
		email = 'testeremail@gmail.com',
		password = 'correct_password'
		)

	user.save()

	return user

def create_known_pcuser():

	user = User.objects.create_user(
		username = 'onetimename',
		email = 'onetimeemail@gmail.com',
		password = 'correct_password'
		)

	pcuser = Pcuser.objects.create(
		user = user,
		location = 'Known location',
		phone = '1234567890',
		gender = 'Female',
		reset_pass = '1',
		verified = '1'
		)
	pcuser.save()

	return pcuser

def get_admins_ordered_alphabetically():

	admin_list = User.objects.all().order_by('username')
	return admin_list

#Note : All pcusers are users, but every user is not a pcuser
def get_pcusers_ordered_alphabetically():

	pcuser_list = Pcuser.objects.all().order_by('user__username')
	return pcuser_list


def search_admins(username, email):

	""" This function searches for the admins. You can give username, email or none for searching
	In case no parameter is provided, it returns the list of all the existing admins
	Example: search_admins(None, None) will return all admins
	search_admins('yo', None) returns all the admins which have 'yo' in their username
	"""

	search_query = User.objects.all()

	if username:
		search_query = search_query.filter(username__contains=username)
	if email:
		search_query = search_query.filter(email__contains=email)

	return search_query	

def search_pcusers(username, email, location, phone, gender):

	"""This function searches for the pcusers existing in the database. You can give the user associated, the email associated
	with the user, location, phone, gender (in any form) or nothing to filter.
	In case of no parameter, it returns all the pcusers.
	Example: search_pcusers(None, None, None, None, 'M') will return all the male pcusers
	"""

	search_query = Pcuser.objects.all()

	if username:
		search_query = search_query.filter(user__username__contains=username)
	if email:
		search_query = search_query.filter(user__email__contains=email)
	if location:
		search_query = search_query.filter(location__contains=location)
	if phone:
		search_query = search_query.filter(phone__contains=phone)
	if gender:
		search_query = search_query.filter(gender__contains=gender)

	return search_query

def delete_random_admins():
	"""This deletes all the random admins created for testing purposes
	For avoiding confusion, this must be called after the tests are cleared up
	"""

	random_query = User.objects.all()
	random_query = random_query.filter(username__startswith='name')
	random_query.delete()
	new_list = User.objects.all()

	return new_list

def delete_random_pcusers():
	"""This deletes all the random pcusers created for the testing purpose
	For avoiding confusion, this must be called after the tests are cleared up
	"""

	random_query = Pcuser.objects.all()
	random_query = random_query.filter(user__username__startswith='name')
	random_query.delete()
	new_list = Pcuser.objects.all()

	return new_list



