from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    uuid = ShortUUIDField(
        primary_key=True,
        editable=False,
        length=6,
        alphabet = '123456789',
    )

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract  = True
        ordering = ['-created']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Brand(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='brand_logos', blank=True, null=True)

    def __str__(self):
        return self.name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProductBase(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_bases')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name='product_bases')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0),MaxValueValidator(100)])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProductVariant(BaseModel): 
    product_base = models.ForeignKey(ProductBase, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255) 
    image = models.ImageField(upload_to='product_variant_images', blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product_base.name} - {self.name}" 


    @property
    def discounted_price(self):
        if self.product_base.discount_percentage: 
            discount_amount = (self.product_base.discount_percentage / 100) * self.price
            return self.price - discount_amount
        return self.price

    @property
    def in_stock(self):
        return self.stock_quantity > 0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ORDER_STATUS_CHOICES = [
    ('PENDING_ORDER', 'Pending Order'),        # Initial state when customer places order
    ('CONTACTED_CUSTOMER', 'Contacted Customer'), # Admin has contacted customer for order details/confirmation
    ('PAYMENT_CONFIRMED_EXT', 'Payment Confirmed (External)'), # Payment confirmed externally (via phone call process)
    ('PROCESSING', 'Processing'),             # Order being processed (packing, etc.)
    ('SHIPPED', 'Shipped'),                    # Order has been shipped
    ('DELIVERED', 'Delivered'),                # Order delivered
    ('CANCELLED', 'Cancelled'),                # Order cancelled
]

class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='PENDING_ORDER') 
    shipping_address = models.TextField()
    billing_address = models.TextField()
    shipped_date = models.DateTimeField(null=True, blank=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=50) 

    def __str__(self):
        return f"Order #{self.uuid} - {self.customer.username} - {self.created.strftime('%Y-%m-%d %H:%M')}"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]) 

    def __str__(self):
        return f"{self.product_variant.product_base.name} - {self.product_variant.name} x {self.quantity} in Order #{self.order.uuid}"

    @property
    def subtotal(self):
        return self.price * self.quantity

  
