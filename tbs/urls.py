from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^register$', views.RegisterView.as_view(), name='register'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
	url(r'^admin_login$', views.AdminLoginView.as_view(), name='admin_login'),
	url(r'^change_password$', views.ChangePasswordView.as_view(), name='change_password'),
	url(r'^sell_item$', views.SellItemView.as_view(), name='sell_item'),
	url(r'^edit_item$', views.EditItemView.as_view(), name='edit_item'),
	url(r'^delete_item$', views.DeleteItemView.as_view(), name='delete_item'),
	url(r'^donate_item$', views.DonateItemView.as_view(), name='donate_item'),
	url(r'^buy_item$', views.BuyItemView.as_view(), name='buy_item'),
	url(r'^cancel_reserved_item$', views.CancelReservedItemView.as_view(), name='cancel_reserved_item'),
	url(r'^get_donated_item$', views.GetDonatedItemView.as_view(), name='get_donated_item'),
	url(r'^admin_approveItem$', views.AdminApproveItemView.as_view(), name='admin_approveItem'),
	url(r'^admin_disapproveItem$', views.AdminDisapproveItemView.as_view(), name='admin_disapproveItem'),
	url(r'^add_category$', views.AddCategoryView.as_view(), name='add_category'),
	url(r'^item_available$', views.ReservedItemAvailableView.as_view(), name='item_available'),
	url(r'^item_claimed$', views.ReservedItemClaimedView.as_view(), name='item_claimed'),
	url(r'^admin_approveDonation$', views.AdminApproveDonationView.as_view(), name='admin_approveDonation'),
	url(r'^admin_disapproveDonation$', views.AdminDisapproveDonationView.as_view(), name='admin_disapproveDonation'),

]