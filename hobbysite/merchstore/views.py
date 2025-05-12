from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from .models import Product, Transaction

class ProductListView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            user_items = Product.objects.filter(owner=profile)
            all_items = Product.objects.exclude(owner=profile)
            ctx.update({'user_items':user_items,'object_list':all_items})
        return ctx

class ProductDetailView(DetailView):
    model = Product
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        form_amount = int(request.POST['amount'])
        if self.object.owner == request.user.profile or self.object.stock < form_amount:
            return self.get(request,*args,**kwargs)
        Transaction.objects.create(
          buyer=request.user.profile,
          product=self.object,
          amount=form_amount
        )
        self.object.stock -= form_amount
        self.object.save()
        return redirect('merchstore:cart')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = [
        'name',
        'product_type',
        'description',
        'price',
        'stock',
        'status'
    ]
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = [
        'name',
        'product_type',
        'description',
        'price',
        'stock',
        'status'
    ]

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name='merchstore/cart.html'
    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.profile)

class SellerTransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name='merchstore/transactions.html'
    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user.profile)
