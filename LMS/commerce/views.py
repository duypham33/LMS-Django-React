from unicodedata import category
from django.shortcuts import render, redirect
from .models import Category, LatestCourseView, CartItem, Order, OrderItem
from app.models import Course
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
import uuid
# Create your views here.


@login_required(login_url='login/')
def index(request):
    categories = Category.objects.all()[0:5]
    courses = Course.objects.filter(active = True).all()

    context = {'categories': categories, 'courses': courses}
    return render(request, 'commerce/index.html', context = context)


@login_required(login_url='login/')
def course_list(request):
    courses = Course.objects.filter(active = True).all()
    
    quer = request.GET.get('query')
    if quer is not None and quer != '':
        courses = Course.objects.filter(active = True).filter(Q(title__icontains = quer)|Q(subject__name__icontains = quer)).all()

    context = {'courses': courses}
    return render(request, 'commerce/course_list.html', context = context)


@login_required(login_url='login/')
def course_detail(request, pk):
    if request.user.get_role().courses.filter(pk = pk).exists() == True:
        return redirect('course:home', pk = pk)  #Have access

    course = Course.objects.get(pk = pk)

    LatestCourseView.objects.create(user = request.user, course = course)
    latest_views = request.user.latest_views.all()

    cats = course.categories.all()
    related_courses = Course.objects.filter(categories__in = cats).exclude(pk = pk).all()
    
    context = {'course': course, 'related_courses': related_courses, 'latest_views': latest_views}
    return render(request, 'commerce/course_detail.html', context = context)



@login_required(login_url='login/')
def add_cart_item(request, pk):
    course = Course.objects.get(pk = pk)
    cart = request.user.cart

    CartItem.objects.create(course = course, cart = cart)
    cart.subtotal += course.final_price()
    cart.save()

    return redirect('commerce:view_cart')


@login_required(login_url='login/')
def remove_cart_item(request, pk):
    item = CartItem.objects.get(pk = pk)
    cart = request.user.cart

    cart.subtotal -= item.course.final_price()
    cart.save()
    item.delete()

    return redirect('commerce:view_cart')


@login_required(login_url='login/')
def view_cart(request):
    return render(request, 'commerce/view_cart.html', context = {'cart': request.user.cart})


@login_required(login_url='login/')
def checkout(request):
    cart = request.user.cart
    if request.method == 'POST':
        ids = [(request.POST.get(f'{item.pk}'), item.pk) for item in cart.items.all()]
        selected_ids = [b for (a, b) in ids if a]
        items = cart.items.filter(pk__in = selected_ids).all()
        
        if items.count() == 0:
            messages.warning(request, 'You need select at least one item to check out!')
            return redirect('commerce:view_cart')

        subtotal = sum([item.course.final_price() for item in items])
    else:
        items = cart.items.all()
        subtotal = cart.subtotal
            
    context = {'items': items, 'subtotal': subtotal}
    return render(request, 'commerce/checkout.html', context = context)



@login_required(login_url='login/')
def single_checkout(request, pk):
    cart = request.user.cart
    course = Course.objects.get(pk = pk)
    items = cart.items.filter(course = course).all()
    subtotal = course.final_price()

    if items.count() == 0:
        #Not in cart
        item, _ = CartItem.objects.get_or_create(course = course, cart = cart)
        cart.subtotal += subtotal
        cart.save()
        items = [item]
        
    context = {'items': items, 'subtotal': subtotal}
    return render(request, 'commerce/checkout.html', context = context)



@login_required(login_url='login/')
def checkout_process(request):
    if request.method == 'POST':
        cart = request.user.cart

        first_name = request.POST.get('billing_first_name')
        last_name = request.POST.get('billing_last_name')
        company = request.POST.get('billing_company')
        country = request.POST.get('billing_country')
        street_address = request.POST.get('billing_address')
        city = request.POST.get('billing_city')
        postcode = request.POST.get('billing_postcode')
        phone = request.POST.get('billing_phone')
        email = request.POST.get('billing_email')
        additional_info = request.POST.get('order_comments')
        payment_method = request.POST.get('payment_method')

        item_ids = request.POST.getlist('items')
        items = cart.items.filter(pk__in = item_ids).all()
        subtotal = Decimal(request.POST.get('subtotal'))
        
        company = None if not company or company == '' else company
        additional_info = None if not additional_info or additional_info == '' else additional_info

        order = Order.objects.create(buyer=request.user, first_name=first_name, last_name=last_name,
        company=company, country=country, street_address=street_address, city=city, postcode=postcode,
        phone=phone, email=email, additional_info=additional_info, payment_method=payment_method,
        subtotal=subtotal)
        order.order_id = str(uuid.uuid4()).replace("-", "").upper()[:8]
        order.save()

        for index, item in enumerate(items):
            course = item.course
            OrderItem.objects.create(order = order, course = course, num = index + 1)
            
            cart.subtotal -= course.final_price()
            cart.save()
            item.delete()

            if request.user.user_type != '1':
                request.user.get_role().enroll(course)  #Now, can access the course

        context = {'order': order, 'mode_order_completed': True}
        return render(request, 'commerce/completed_order.html', context = context)


@login_required(login_url='login/')
def view_orders(request):
    orders = request.user.orders if request.user.orders else None
    context = {'orders': orders}
    return render(request, 'commerce/view_orders.html', context = context)


@login_required(login_url='login/')
def order_detail(request, pk):
    order = Order.objects.get(pk = pk)
    context = {'order': order, 'mode_order_completed': True}
    return render(request, 'commerce/completed_order.html', context = context)