from django.db import models
from user_management.models import Profile

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
        null=True,
        blank=True
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    STATUS_CHOICES = [
        ('available','Available'),
        ('on_sale','On sale'),
        ('out_of_stock','Out of stock'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='available')
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status='out_of_stock'
        elif self.status=='out_of_stock' and self.stock>0:
            self.status='available'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchases'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.PositiveIntegerField()
    STATUS_CHOICES = [
      ('on_cart','On cart'),
      ('to_pay','To Pay'),
      ('to_ship','To Ship'),
      ('to_receive','To Receive'),
      ('delivered','Delivered'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='on_cart')
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.buyer}→{self.product}×{self.amount}"