from django.test import TestCase
from django.contrib.auth.models import User


from signup.models import Pcuser
from signup.utils import (create_random_admin, create_random_pcuser,
							create_known_admin, create_known_pcuser,
							get_admins_ordered_alphabetically,
							get_pcusers_ordered_alphabetically,
							search_admins, search_pcusers,
							delete_random_admins)

# Create your tests here.

class PcuserModelTest(TestCase):

	def test_saving_and_retrieving_users(self):

		user = User.objects.create_user(username='testusername', 
								email='testuseremail@gmail.com', 
								password='testpassword')
		user.save()

		saved_users = User.objects.all()
		new_user = User.objects.first()
		self.assertEqual(new_user, user)
		self.assertEqual(saved_users.count(), 1)

	def test_saving_multiple_users(self):

		user_1 = User.objects.create_user(username='username1',
								email='username1@gmail.com',
								password='password_1'
								)
		user_1.save()

		saved_users = User.objects.all()
		new_user = User.objects.first()
		self.assertEqual(new_user, user_1)
		self.assertEqual(saved_users.count(), 1)

		user_2 = User.objects.create_user(username='username2',
								email='username2@gmail.com',
								password='password_2'
								)
		user_2.save()

		saved_users = User.objects.all()
		new_user = User.objects.last()
		old_user = User.objects.first()
		self.assertEqual(new_user, user_2)
		self.assertEqual(old_user, user_1)
		self.assertEqual(saved_users.count(), 2)

	def test_checking_one_random_user(self):

		create_random_admin()
		admin_list = User.objects.all()
		new_admin = User.objects.last()
		self.assertEqual(admin_list.count(), 1)
		self.assertIn('name', new_admin.username)

	def test_checking_nultiple_random_users(self):

		create_random_admin()
		create_random_admin()
		admin_list = User.objects.all()
		self.assertEqual(admin_list.count(), 2)

		create_random_admin()
		admin_list = User.objects.all()
		self.assertEqual(admin_list.count(), 3)


	def test_search_admin_runs_properly(self):

		create_random_admin()
		create_random_admin()
		create_random_admin()

		hardcoded_user = User.objects.create_user(username='hardcoded',
										email='hardcoded@gmail.com',
										password='correct_password'
										)
		hardcoded_user.save()

		user_list = User.objects.all()
		self.assertEqual(user_list.count(), 4)
		self.assertEqual(search_admins('name', None).count(), 3)

		random_queryset = search_admins('name', None)
		self.assertEqual(random_queryset.count(), 3)

	def test_saving_and_retrieving_pcusers(self):

		user = User.objects.create_user(username='testpcuser',
								email='testpc@gmail.com',
								password='password_1'
								)
		pcuser = Pcuser.objects.create(
						user=user,
						location='Known test location',
						phone='999999',
						gender='Female',
						reset_pass='1',
						verified='1'
						)
		pcuser.save()

		pcuser_list = Pcuser.objects.all()
		new_pcuser = Pcuser.objects.last()

		self.assertEqual(pcuser_list.count(), 1)
		self.assertEqual(new_pcuser, pcuser)
		self.assertEqual(new_pcuser.user, user)
		self.assertEqual(new_pcuser.user.username, 'testpcuser')
		self.assertEqual(new_pcuser.user.email, 'testpc@gmail.com')
		self.assertEqual(new_pcuser.gender, 'Female')

	def saving_mulitple_pcusers(self):

		user_1 = User.objects.create_user(username='username1',
									email='username1@gmail.com',
									password='password_1'
									)
		pcuser_1 = Pcuser.objects.create(
						user=user_1,
						location='Location one',
						phone='12345678',
						gender='Male',
						reset_pass='1',
						verified='1'
						)
		pcuser_1.save()

		pcuser_list = Pcuser.objects.all()
		user_list = User.objects.last()
		new_pcuser = Pcuser.objects.last()

		self.assertEqual(pcuser_list.count(), 1)
		self.assertEqual(user_list.username, new_pcuser.user.username)
		self.assertEqual(new_pcuser.user.username, 'username1')

		user_2 = User.objects.create(
						username='username2',
						email='username2@gmail.com',
						password='passowrd_2'
						)

		pcuser_2 = Pcuser.objects.create(
					user=user_2,
					location='Location two',
					phone='78903484',
					gender='Female',
					reset_pass='1',
					verified='1'
					)
		pcuser_2.save()

		pcuser_list = Pcuser.objects.all()
		user_list = User.objects.all()
		new_user = User.objects.last()
		new_pcuser = Pcuser.objects.last()

		self.assertEqual(pcuser_list.count(), 2)
		self.assertEqual(user_list.count(), 2)
		self.assertEqual(new_user.username, 'username2')
		self.assertEqual(new_pcuser.user.username, 'username2')
		self.assertEqual(new_pcuser.user.username, new_user.username)
		self.assertEqual(new_pcuser.phone, '78903484')


	def test_checking_one_random_pcuser(self):

		create_random_pcuser()
		pcuser_list = Pcuser.objects.all()
		last_pcuser = Pcuser.objects.last()
		self.assertEqual(pcuser_list.count(), 1)
		self.assertIn('name', last_pcuser.user.username)


	def test_checking_mulitple_random_pcusers(self):

		create_random_pcuser()
		create_random_pcuser()
		create_random_pcuser()
		pcuser_list = Pcuser.objects.all()
		self.assertEqual(pcuser_list.count(), 3)

		create_random_pcuser()
		create_random_pcuser()
		pcuser_list = Pcuser.objects.all()
		self.assertEqual(pcuser_list.count(), 5)


	def test_search_pcuser_runs_properly(self):

		create_random_pcuser()
		create_random_pcuser()
		create_random_pcuser()

		hardcoded_user = User.objects.create_user(
							username='hardcoded',
							email='hardcoded1@gmail.com',
							password='hardcoded'
							)

		hardcoded_pcuser = Pcuser.objects.create(
							user=hardcoded_user,
							location='Hardcoded location for pcuser',
							phone='839489340',
							gender='Male',
							reset_pass='1',
							verified='1'
							)
		hardcoded_pcuser.save()

		pcuser_list = Pcuser.objects.all()
		self.assertEqual(pcuser_list.count(), 4)

		random_queryset = search_pcusers('name', None, None, None, None)
		self.assertEqual(random_queryset.count(), 3)


	def test_admin_list_alphabetically(self):

		user_1 = User.objects.create_user(
							username='banana',
							email='banana@gmail.com',
							password='password'
							)
		user_2 = User.objects.create_user(
							username='apple',
							email='apple@gmail.com',
							password='password'
							)
		user_1.save()
		user_2.save()

		sorted_list = get_admins_ordered_alphabetically()

		self.assertEqual(sorted_list.first().username, 'apple')


	def test_pcuser_list_alphabetically(self):

		user_1 = User.objects.create_user(username='banana',
								email='username1@gmail.com',
								password='password_1'
								)
		pcuser_1 = Pcuser.objects.create(
						user=user_1,
						location='Location one',
						phone='12345678',
						gender='Male',
						reset_pass='1',
						verified='1'
						)
		pcuser_1.save()

		user_2 = User.objects.create(
						username='apple',
						email='username2@gmail.com',
						password='passowrd_2'
						)

		pcuser_2 = Pcuser.objects.create(
					user=user_2,
					location='Location two',
					phone='78903484',
					gender='Female',
					reset_pass='1',
					verified='1'
					)
		pcuser_2.save()

		sorted_list = get_pcusers_ordered_alphabetically()

		self.assertEqual(sorted_list.first().user.username, 'apple')


	def test_deleting_random_users(self):

		create_random_admin()
		create_random_admin()
		create_random_admin()

		user_list = User.objects.all()
		self.assertEqual(user_list.count(), 3)

		delete_random_admins()

		user_list = User.objects.all()
		self.assertEqual(user_list.count(), 0)















 





