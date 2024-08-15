from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import CategoryListView, CustomLoginView, ProductListView, ProductDetailView, WishListView, \
    LikeProductView, OrderListView, MarketListView, StreamFormView, QuestionView, CompetitionView, \
    PaymentView, StreamListView, StreamOrderView, StreamStatisticListView, StreamDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('product/list', ProductListView.as_view(), name='product-list'),
    path('product/detail/<str:slug>', ProductDetailView.as_view(), name='product-detail'),

    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('wishlist', WishListView.as_view(), name='wish-list'),

    path('product/liked/<str:slug>', LikeProductView.as_view(), name='liked'),
    path('product/order-list', OrderListView.as_view(), name='order-list'),

    path('product/market-list', MarketListView.as_view(), name='market-list'),
]
urlpatterns += [
    path('product/stream-form', StreamFormView.as_view(), name='stream-form'),
    path('product/stream-list', StreamListView.as_view(), name='stream-list'),
    path('product/stream-detail/<str:slug>', StreamDetailView.as_view(), name='stream-detail'),
    path('oqim/<int:pk>', StreamOrderView.as_view(), name='stream-order'),
    path('product/stream-statistic', StreamStatisticListView.as_view(), name='stream-statistic'),

]

urlpatterns += [
    path('product/questions', QuestionView.as_view(), name='question-list'),
    path('product/competition', CompetitionView.as_view(), name='competition-list'),
    path('product/payment', PaymentView.as_view(), name='payment-list'),

]
