from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F, Sum
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import ProductForm, RegistrationForm
from .models import Product, CartItem


def product_list(request):
    return render(request, 'store/product_list.html', {'products': Product.objects.all().order_by('-created_at')})


def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'store/add_product.html', {'form': form})


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('product_list')
    return render(request, 'registration/register.html', {'form': form})


class ShopLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class ShopLogoutView(LogoutView):
    next_page = reverse_lazy('product_list')


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Исходная модель корзины общая для всех: разделение по пользователям
    # требует отдельной миграции. Здесь сохраняется исходное поведение.
    item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        item.quantity = F('quantity') + 1
        item.save(update_fields=['quantity'])
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.select_related('product').all()
    total_price = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
@require_POST
def clear_cart(request):
    CartItem.objects.all().delete()
    return redirect('cart')
