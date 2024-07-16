from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from django.contrib import messages
from django.core.paginator import Paginator
from .serializers import *
from .models import *


def home(request):
    return render(request, 'shop/index.html')


def user_home(request):
    return render(request, 'shop/user_index.html')


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        mobile_number = request.POST.get('pass')

        try:
            customer = Customer.objects.get(name=name, mobile_number=mobile_number)
            request.session['customer_id'] = customer.id
            return redirect('home')  # Redirect to a home page or dashboard
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or mobile number.')

    return render(request, 'shop/login.html')


def product_list(request):
    products = Product.objects.all()
    variants = Variant.objects.all()
    paginator = Paginator(products, 3)  # Show 10 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'page_obj': page_obj, 'variants': variants})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import SalesOrder, Product, Variant, Customer


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))

    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'You must be logged in to add items to the cart.')
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if variant_id is provided; if not, set variant to None
    variant = None
    if variant_id:
        variant = get_object_or_404(Variant, id=variant_id)
    SalesOrder.objects.create(
        customer=customer,
        product=product,
        variant=variant,
        qty=quantity,
        price=product.sales_price,  # Use sale price or original price as needed
    )

    messages.success(request, 'Product added to cart successfully.')
    return redirect('products')


def cart_detail(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        messages.error(request, 'You need to log in to view your cart.')
        return redirect('login')

    customer = Customer.objects.get(id=customer_id)
    orders = SalesOrder.objects.filter(customer=customer)

    return render(request, 'shop/view_cart.html', {
        'customer': customer,
        'orders': orders
    })


def remove_from_cart(request, order_id):
    if request.method == 'POST':
        SalesOrder.objects.filter(id=order_id).delete()
        messages.success(request, 'Item removed from cart.')
        return redirect('view_cart')


def checkout(request):
    order = SalesOrder.objects.filter(customer=request.user.email).first()
    if request.method == 'POST':
        # Save customer details and ordered items
        order.customer_name = request.POST.get('name')
        order.customer_email = request.POST.get('email')
        order.save()
        return redirect('order_complete')
    return render(request, 'shop/checkout.html', {'order': order})


def order_complete(request):
    return render(request, 'shop/order_complete.html')


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductSerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VariantList(generics.ListCreateAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class VariantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
