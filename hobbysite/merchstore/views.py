from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Transaction, ProductType
from .forms import ProductForm, TransactionForm
from user_management.models import Profile


def product_list(request):
    all_products = Product.objects.select_related('product_type', 'owner__user').all().order_by('name')

    user_products = None
    other_products = all_products

    if request.user.is_authenticated:
        user_profile = request.user.profile
        user_products = all_products.filter(owner=user_profile)
        other_products = all_products.exclude(owner=user_profile)

    context = {
        'user_products': user_products,
        'other_products': other_products,
    }
    return render(request, 'merchstore/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user = request.user
    user_profile = getattr(user, 'profile', None)
    is_owner = user.is_authenticated and product.owner == user_profile
    can_buy = user.is_authenticated and not is_owner and product.stock > 0

    form = TransactionForm()

    if request.method == 'POST':
        if not user.is_authenticated:
            return redirect(f'/login/?{REDIRECT_FIELD_NAME}={request.path}')

        form = TransactionForm(request.POST)
        if form.is_valid() and can_buy:
            trans = form.save(commit=False)
            trans.buyer = user_profile
            trans.product = product

            if trans.amount > product.stock:
                form.add_error('amount', 'Not enough stock available.')
            else:
                trans.save()
                product.stock -= trans.amount
                product.save()
                return redirect('merchstore:cart')

    context = {
        'product': product,
        'form': form,
        'can_buy': can_buy,
        'is_owner': is_owner,
    }
    return render(request, 'merchstore/product_detail.html', context)


@login_required
def product_create(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.owner = request.user.profile
            prod.save()
            return redirect('merchstore:product-detail', pk=prod.pk)
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'merchstore/product_form.html', context)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user.profile:
        return redirect('merchstore:product-detail', pk=pk)

    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            prod = form.save(commit=False)

            if prod.stock == 0:
                prod.status = 'Out of stock'
            else:
                prod.status = 'Available'

            prod.save()
            return redirect('merchstore:product-detail', pk=prod.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'merchstore/product_form.html', {'form': form, 'product': product})


@login_required
def cart(request):
    items = Transaction.objects.select_related('product__owner').filter(
        buyer=request.user.profile, status='on_cart'
    )

    grouped = defaultdict(list)
    for item in items:
        grouped[item.product.owner].append(item)

    context = {'grouped_transactions': grouped.items(),}
    return render(request, 'merchstore/cart.html', context)



@login_required
def transactions(request):
    items = Transaction.objects.filter(
        product__owner=request.user.profile).exclude(status='on_cart')
    context = {'transactions': items}
    return render(request, 'merchstore/transactions.html', context)
