# Generated by Django 5.1.6 on 2025-02-26 10:02

import django.core.validators
import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brand_logos')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('shipping_address', models.TextField(blank=True)),
                ('billing_address', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('PENDING_ORDER', 'Pending Order'), ('CONTACTED_CUSTOMER', 'Contacted Customer'), ('PAYMENT_CONFIRMED_EXT', 'Payment Confirmed (External)'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PENDING_ORDER', max_length=30)),
                ('shipping_address', models.TextField()),
                ('billing_address', models.TextField()),
                ('shipped_date', models.DateTimeField(blank=True, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('payment_method', models.CharField(max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductBase',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_bases', to='main.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_bases', to='main.category')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_variant_images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('stock_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('product_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='main.productbase')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet='123456789', editable=False, length=6, max_length=6, prefix='', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productvariant')),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
        ),
    ]
