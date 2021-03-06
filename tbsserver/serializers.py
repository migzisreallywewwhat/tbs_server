from django.contrib.auth.models import User

from tbs import models

from rest_framework import serializers, viewsets


class StudentSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Student
		fields = 'id_number', 'first_name', 'last_name', 'course'


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = 'username', 'is_staff'


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False)
	student = StudentSerializer(many=False)

	class Meta:
		model = models.UserProfile
		fields = 'user', 'student', 'stars_collected'


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Category
		fields = 'id','category_name',


class ItemSerializer(serializers.ModelSerializer):
	owner = UserProfileSerializer(many=False)
	category = CategorySerializer(many=False)

	class Meta:
		model = models.Item
		fields = 'id','owner', 'name', 'description', 'category', 'status', 'purpose', 'price', 'picture', 'stars_required'


class NotificationSerializer(serializers.ModelSerializer):
	target = UserSerializer(many=False)
	maker = UserSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.Notification
		fields = 'target','maker', 'item', 'message', 'notification_type', 'status', 'notification_date'


class TransactionSerializer(serializers.ModelSerializer):
	item = ItemSerializer(many=False)
	buyer = UserProfileSerializer(many=False)
	seller = UserProfileSerializer(many=False)

	class Meta:
		model = models.Transaction
		fields = 'id','item', 'buyer', 'seller', 'date_claimed'


class SellApprovalSerializer(serializers.ModelSerializer):
	seller = UserSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ApprovalSellRequest
		fields = 'id','seller', 'item', 'request_date', 'request_expiration'


class DonateApprovalSerializer(serializers.ModelSerializer):
	donor = UserSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ApprovalDonateRequest
		fields = 'id','donor', 'item', 'request_date', 'request_expiration'


class ReservationSerializer(serializers.ModelSerializer):
	buyer = UserSerializer(many=False)
	item = ItemSerializer(many=False)

	class Meta:
		model = models.ReservationRequest
		fields = 'id','buyer', 'item', 'reserved_date', 'request_expiration', 'status'


class UserNotificationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Notification.objects.all()
	serializer_class = NotificationSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Notification.objects.filter(target__username__iexact=username, status="unread")

		return super(UserNotificationViewSet, self).get_queryset()


class AdminNotificationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Notification.objects.all()
	serializer_class = NotificationSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Notification.objects.filter(target__username__iexact=username,target__is_staff=True)

		return super(AdminNotificationViewSet, self).get_queryset()


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.UserProfile.objects.all()
	serializer_class = UserProfileSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username',None)

		if username is not None:
			return models.UserProfile.objects.filter(user__username__iexact = username)

		return super(UserProfileViewSet, self).get_queryset()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Transaction.objects.all()
	serializer_class = TransactionSerializer


class SellApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ApprovalSellRequest.objects.filter()
	serializer_class = SellApprovalSerializer

	def get_queryset(self):
		request_id = self.request.query_params.get('request_id',None)

		if request_id is not None:
			return models.ApprovalSellRequest.objects.filter(id = request_id)

		return super(SellApprovalViewSet, self).get_queryset()


class DonateApprovalViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ApprovalDonateRequest.objects.all()
	serializer_class = DonateApprovalSerializer

	def get_queryset(self):
		request_id = self.request.query_params.get('request_id',None)

		if request_id is not None:
			return models.ApprovalDonateRequest.objects.filter(id = request_id)

		return super(DonateApprovalViewSet, self).get_queryset()


class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.ReservationRequest.objects.all()
	serializer_class = ReservationSerializer

	def get_queryset(self):
		request_id = self.request.query_params.get('request_id',None)

		if request_id is not None:
			return models.ReservationRequest.objects.filter(id = request_id)

		return super(ReservationViewSet, self).get_queryset()

#User: Sell Items
class ItemsToSellViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, status="Available", purpose="Sell")

		return super(ItemsToSellViewSet, self).get_queryset()

#User: Pending Items
class PendingItemsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, status="Pending")

		return super(PendingItemsViewSet, self).get_queryset()

#User: Buy Items
class AvailableItemsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(status="Available", purpose="Sell").exclude(owner__user__username__iexact = username)

		return super(AvailableItemsViewSet, self).get_queryset()

#User: Donate Items
class ItemsToDonateViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(owner__user__username__iexact = username, status="Available", purpose="Donate")

		return super(ItemsToDonateViewSet, self).get_queryset()

#User: Claim Award button
class AllDonationsViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		username = self.request.query_params.get('username', None)

		if username is not None:
			return models.Item.objects.filter(status="Available", purpose="Donate").exclude(owner__user__username__iexact = username)

		return super(AllDonationsViewSet, self).get_queryset()


class ListCategoriesViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Category.objects.all()
	serializer_class = CategorySerializer


class SearchItemViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		queryset = models.Item.objects.all()

		query = self.request.query_params.get('search', None)
		if query is not None:
			queryset.filter(name__icontains=query)

		return queryset

#User: Categorize
class CategorizeViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Item.objects.all()
	serializer_class = ItemSerializer

	def get_queryset(self):
		category = self.request.query_params.get('category', None)

		if category is not None:
			return models.Item.objects.filter(category__category_name=category)

		return super(AllDonationsViewSet, self).get_queryset()