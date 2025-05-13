from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Transaction, ProductType
from .forms import ProductForm, TransactionForm
from user_management.models import Profile


@login_required
def product_list(request):
    all_products = Product.objects.select_related('product_type').all().order_by('name')
    user_profile = request.user.profile
    user_products = all_products.filter(owner=user_profile)
    other_products = all_products.exclude(owner=user_profile)

    context = {
        'user_products': user_products,
        'other_products': other_products,
    }
    return render(request, 'merchstore/product_list.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    can_buy = (product.owner != request.user.profile and product.stock > 0)
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid() and can_buy:
            trans = form.save(commit=False)
            trans.buyer = request.user.profile
            trans.product = product
            trans.save()
            product.stock -= trans.amount
            product.save()
            return redirect('merchstore:cart')

    context = {
        'product': product,
        'form': form,
        'can_buy': can_buy,
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
            prod = form.save()
            return redirect('merchstore:product-detail', pk=prod.pk)

    context = {'form': form, 'product': product}
    return render(request, 'merchstore/product_form.html', context)


@login_required
def cart(request):
    items = Transaction.objects.filter(
        buyer=request.user.profile, status='on_cart')
    context = {'transactions': items}
    return render(request, 'merchstore/cart.html', context)


@login_required
def transactions(request):
    items = Transaction.objects.filter(
        product__owner=request.user.profile).exclude(status='on_cart')
    context = {'transactions': items}
    return render(request, 'merchstore/transactions.html', context)
