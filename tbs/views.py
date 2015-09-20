from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile, Student, Notification, Transaction, ApprovalSellRequest, Item, Category
from django.contrib.auth import authenticate
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import QueryDict


class RegisterView(View):
	def post(self, request):
		id_number = request.POST.get('id_number',None)
		first_name = request.POST.get('first_name',None)
		last_name = request.POST.get('last_name',None)
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if id_number and first_name and last_name and username and password:
			try:
				student = Student.objects.get(id_number=id_number,first_name__iexact=first_name,last_name__iexact=last_name)

				user_profile = UserProfile()

				user = User()
				user.username = username
				user.set_password(password)
				user.first_name = first_name
				user.last_name = last_name
				user.save()

				user_profile.user = user
				user_profile.student = student
				user_profile.save()

				response = {
					'status': 201,
					'statusText': 'User created',
				}
			except Student.DoesNotExist:
				response = {
					'status': 404,
					'statusText': 'User does not exist',
				}
			
			return JsonResponse(response)
		else:

			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'registration.html')


class LoginView(View):
	def post(self, request):
		print(request.body)

		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if username is None or password is None:
			response = {
				'status': 404,
				'statusText': 'Invalid input',
			}
			return JsonResponse(response)
		else:
			user =  authenticate(username=username,password=password).id
			if user is not None:
				response = {
					'status': 200,
					'statusText': 'Successful Login',
					'user_id': user,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'Invalid username or password',
				}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'login.html')


class AdminLoginView(View):
	def post(self, request):

		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if username is None or password is None:
			response = {
				'status': 404,
				'statusText': 'Missing username or password',
			}
			return JsonResponse(response)
		else:
			user =  authenticate(username=username,password=password)
			if user is not None and user.is_staff:
				response = {
					'status': 200,
					'statusText': 'Successful Login',
				}
			else:
				response = {
					'status': 403,
					'statusText': 'Invalid username or password--> Not admin',
				}
			return JsonResponse(response)

	def get(self, request):
		return render(request, 'adminLogin.html')


class ProfileView(View):
	def get(self, request):
		print(request.body)

		user_id = request.GET.get('user_id',None)
		print(user_id)
		if user_id is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			user_id = UserProfile.objects.get(user=user_id)

			serializer = UserProfileSerializer(user_id)
			data = serializer.data
			if user_id is not None:
				response = {
					'status': 200,
					'statusText': 'Profile found',
					'data': data,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'UserProfile not found',
				}
			return JsonResponse(response)


class ChangePasswordView(View):
	def put(self, request):
		put = QueryDict(request.body)
		username = put.get('username',None)
		old_password = put.get('old_password',None)
		new_password = put.get('new_password',None)
		confirm_password = put.get('confirm_password',None)

		if username and old_password and new_password and confirm_password:
			user =  authenticate(username=username,password=old_password)
			if user is not None:
				if new_password == confirm_password:
					user.set_password(new_password)
					user.save()

					response = {
						'status': 200,
						'statusText': 'Password changed',
					}
				else:
					response = {
						'status': 400,
						'statusText': 'Passwords do not match',
					}
			else:
				response = {
					'status': 404,
					'statusText': 'User does not exist',
				}
			
			return JsonResponse(response)
		else:
			response = {
				'status': 403,
				'statusText': 'Some input parameters are missing.',
			}
			return JsonResponse(response)

	def get(self, request):
		print("get")
		return render(request, 'changePassword.html')


class NotificationView(View):
	def get(self, request):

		username = request.GET.get('username',None)
		if username is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			notif = Notification.objects.filter(user__username=username)
			if notif is not None:
				data = NotificationSerializer(notif,many=True).data
				response = {
					'status': 200,
					'statusText': 'There is a notification',
					'data': data,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'You have no notification',
				}
			return JsonResponse(response)


class TransactionView(View):
	def get(self, request):
		transactions = Transaction.objects.all()
		if transactions is not None:
			data = TransactionSerializer(transactions,many=True).data
			response = {
				'status': 200,
				'statusText': 'There is a Transaction',
				'data': data,
			}
		else:
			response = {
				'status': 403,
				'statusText': 'No transactions',
			}
		return JsonResponse(response)


class AllSellApprovalView(View):
	def get(self, request):
		requests = ApprovalSellRequest.objects.all()
		if requests is not None:
			data = SellApprovalSerializer(requests,many=True).data
			response = {
				'status': 200,
				'statusText': 'There is a request',
				'data': data,
			}
		else:
			response = {
				'status': 403,
				'statusText': 'No request',
			}
		return JsonResponse(response)


class AllDonateApprovalView(View):
	def get(self, request):
		requests = ApprovalDonateRequest.objects.all()
		if requests is not None:
			data = DonateApprovalSerializer(requests,many=True).data
			response = {
				'status': 200,
				'statusText': 'There is a request',
				'data': data,
			}
		else:
			response = {
				'status': 403,
				'statusText': 'No request',
			}
		return JsonResponse(response)


class SellApprovalView(View):
	def get(self, request):
		username = request.GET.get('username',None)
		if username is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			requests = ApprovalSellRequest.objects.filter(seller__username=username)
			if requests is not None:
				data = SellApprovalSerializer(requests,many=True).data
				response = {
					'status': 200,
					'statusText': 'There is a request',
					'data': data,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'You have no request',
				}
			return JsonResponse(response)

class SellItemView(View):
	def post(self, request):
		owner = request.POST.get('owner',None)
		name = request.POST.get('name',None)
		description = request.POST.get('description',None)
		#category = request.POST.get('category',None)
		#status = request.POST.get('status',None)
		#purpose = request.POST.get('purpose',None)
		price = request.POST.get('price',None)
		#picture = request.POST.get('picture',None)
		#stars_required = request.POST.get('stars_required',None)

		user = User.objects.get(username=owner)
		if user is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			item_owner = UserProfile.objects.get(user=user)

			approval_sell_request = ApprovalSellRequest()

			item = Item()
			item.owner = item_owner
			item.name = name
			item.description = description
			item.category = Category.objects.get(category_name="Others")
			item.status = "Pending"
			item.purpose = "Sell"
			item.price = price
			item.picture = "https://www.google.com.ph"
			item.stars_required = 0

			item.save()

			approval_sell_request.seller = item_owner
			approval_sell_request.item = item
			approval_sell_request.save()


			admin = User.objects.get(username="admin")
			notif = Notification()
			notif.target = admin
			notif.maker = item_owner
			notif.item = item
			notif.message = "Sell " + item.name
			notif.notification_type = "sell"
			notif.status = "unread"
			notif.save()

			response = {
				'status': 201,
				'statusText': 'Item created',
			}

			return JsonResponse(response)

	def get(self, request):
		return render(request, 'sellItem.html')

class ItemsToSellView(View):
	def get(self, request):

		username = request.GET.get('username',None)
		if username is None :
			response = {
				'status': 404,
				'statusText': 'No username to refer to',
			}
			return JsonResponse(response)
		else:
			item = Item.objects.filter(user__username=username)
			if item is not None:
				data = ItemSerializer(item,many=True).data
				response = {
					'status': 200,
					'statusText': 'There is an item',
					'data': data,
				}
			else:
				response = {
					'status': 403,
					'statusText': 'You have no item',
				}
			return JsonResponse(response)