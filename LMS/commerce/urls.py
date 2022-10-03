
from django.urls import path
from . import views

app_name="commerce"

urlpatterns = [
    path("", views.index, name='index'),
    path("course/list", views.course_list, name='course_list'),
    path("course/<int:pk>", views.course_detail, name='course_detail'),

    path("course/<int:pk>/addcart", views.add_cart_item, name='add_cart_item'),
    path("item/<int:pk>/remove", views.remove_cart_item, name='remove_cart_item'),
    path("mycart", views.view_cart, name='view_cart'),
    path("checkout", views.checkout, name='checkout'),
    path("course/<int:pk>/checkout", views.single_checkout, name='single_checkout'),
    path("checkout/process", views.checkout_process, name='checkout_process'),

    path("orders", views.view_orders, name='view_orders'),
    path("order/<int:pk>", views.order_detail, name='order_detail'),
]