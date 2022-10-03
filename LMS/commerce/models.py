from email.policy import default
from random import choices
from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50)
    icon = models.CharField(max_length = 20, blank = True, null = True)

    def __str__(self):
        return self.name


class LatestCourseView(models.Model):
    user = models.ForeignKey(to = 'app.User', related_name = 'latest_views',
                             on_delete = models.CASCADE, null = True, blank = True)
    course = models.ForeignKey(to = 'app.Course', related_name = 'latest_views',
                             on_delete = models.CASCADE, null = True, blank = True)
    order = models.PositiveIntegerField(default = 1)

    class Meta:
        ordering = ['-order']


class Cart(models.Model):
    user = models.OneToOneField('app.User', related_name = 'cart', on_delete = models.CASCADE,
                                            blank = True, null = True)
    subtotal = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0.0)

    def __str__(self):
        return f'Cart-{self.pk}'
    

class CartItem(models.Model):
    course = models.ForeignKey(to = 'app.Course', related_name = 'carts', on_delete = models.CASCADE,
                                    blank = True, null = True)
    cart = models.ForeignKey(to = Cart, related_name = 'items', on_delete = models.CASCADE,
                                    blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-date_added']



class Order(models.Model):
    order_id = models.CharField(max_length = 30, blank = True)
    buyer = models.ForeignKey(to = 'app.User', related_name = 'orders', on_delete = models.SET_NULL,
                            blank = True, null = True)
    
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    company = models.CharField(max_length = 200, null = True, blank = True)
    country = models.CharField(max_length = 50)
    street_address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 100)
    postcode = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 50)
    additional_info = models.TextField(max_length = 500, null = True, blank = True)

    subtotal = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0.0)
    method = (('Direct bank transfer', 'Direct bank transfer'), ('Check payments', 'Check payments'),
                ('PayPal', 'PayPal'))
    payment_method = models.CharField(max_length = 20, choices = method, default = 'Check payments')
    date_paid = models.DateTimeField(auto_now_add = True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name = 'items', on_delete = models.SET_NULL,
                            blank = True, null = True)
    course = models.ForeignKey(to = 'app.Course', related_name = 'orders', on_delete = models.SET_NULL,
                                    blank = True, null = True)
    num = models.PositiveIntegerField(default = 1)

    class Meta:
        ordering = ['num']