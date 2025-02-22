from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('shop') 
        else:
            messages.error(request, 'Username yoki password xato!')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Siz muvaffaqiyatli chiqdingiz!')
    return redirect('login')





@login_required
def shop_view(request):
    categories = models.Category.objects.all()
    brands = models.Brand.objects.all()
    products = models.ProductVariant.objects.all().order_by('created')
    
    search_query = request.GET.get('search_query')
    category_filter = request.GET.getlist('category_filter')
    brand_filter = request.GET.getlist('brand_filter')

    if brand_filter:
        products = products.filter(product_base__brand__uuid__in=brand_filter)
    
    if category_filter:
        products = products.filter(product_base__category__uuid__in=category_filter)
    
    if search_query:
        products = products.filter(product_base__name__icontains=search_query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        'brands': brands,
        'products': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'brand_filter': brand_filter,       
    }

    return render(request, 'shop.html', context)

@login_required
def product_detail_view(request, uuid):
    product = models.ProductVariant.objects.get(uuid=uuid)

    return render(request, 'product_detail.html', {'product':product})




@login_required
def orders_view(request):
    orders = models.Order.objects.filter(customer = request.user).order_by('created')
    
    return render(request, 'orders.html', {'orders':orders})



@login_required
def cancel_order_view(request, uuid):
    order = get_object_or_404(models.Order, uuid=uuid, customer=request.user)
    
    if order.order_status == 'PENDING_ORDER':
        order.order_status = 'CANCELLED'
        order.save()
        messages.success(request, f"Order #{order.uuid} bekor qilindi!")
    else:
        messages.error(request, f"Order #{order.uuid} bekor qilinmadi. Faqat 'PENDING_ORDER' holatidagi buyurtmalarni bekor qilish mumkin.")
    
    return redirect('orders')




@login_required
def order_detail(request, uuid):
    order = models.OrderItem.objects.get(uuid=uuid)
    
    return render(request, 'order_detail.html', {'order':order})

@login_required
def profile_view(request):
    try:
        profile = models.CustomerProfile.objects.get(user=request.user)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return render(request, 'error.html', {'error': str(e)})
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.shipping_address = request.POST.get('shipping_address')
        profile.billing_address = request.POST.get('billing_address')
        profile.save()
        return redirect('profile') 
    
    return render(request, 'profile.html', {'profile': profile})



@login_required
def buy_now_view(request, uuid):
    product = get_object_or_404(models.ProductVariant, uuid=uuid)
    
    profile = models.CustomerProfile.objects.get(user=request.user)
    
    order = models.Order.objects.create(
        customer=request.user,
        shipping_address=profile.shipping_address,
        billing_address=profile.billing_address,
        total_amount=product.price,
        payment_method='CASH'
    )
    
    models.OrderItem.objects.create(
        order=order,
        product_variant=product,
        quantity=1,
        price=product.price
    )
    
    messages.success(request, f"{product.product_base.name} - {product.name} buyurtmangizga qo'shildi!")
    
    return redirect('orders')  # Buyurtmalar sahifasiga yo'naltirish