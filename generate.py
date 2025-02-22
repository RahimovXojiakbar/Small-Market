import os
import random
import django
from random import choice



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from faker import Faker
from main import models

models.Category.objects.all().delete()
models.Brand.objects.all().delete()
models.ProductBase.objects.all().delete()
models.ProductVariant.objects.all().delete()



fake = Faker()



for _ in range(10):
    categories = models.Category.objects.create(
        name = fake.word().capitalize(),
        description = fake.text(max_nb_chars=100),
    )
    categories.save()
models.Category.objects.all()
print('Add categories')

# brand_logos = [
#     '/brand_logos/istockphoto-165968605-1024x1024.jpg', 
#     '/brand_logos/istockphoto-166082323-1024x1024.jpg', 
#     '/brand_logos/istockphoto-472330663-1024x1024.jpg', 
#     '/brand_logos/istockphoto-490586402-1024x1024.jpg', 
#     '/brand_logos/istockphoto-598141630-1024x1024.jpg', 
#     '/brand_logos/istockphoto-657672288-1024x1024.jpg', 
#     '/brand_logos/istockphoto-960107412-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1126122253-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1148992001-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1225522618-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1315926501-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1341559826-1024x1024.jpg', 
#     '/brand_logos/istockphoto-1341561048-1024x1024.jpg'
# ]




for _ in range(10):
    brands = models.Brand.objects.create(
        name = fake.word().capitalize(),
        # logo = random.choice(brand_logos),
    )
    brands.save()
models.Brand.objects.all()
print('Add brands')



for _ in range(20):
    product_base = models.ProductBase.objects.create(
        name = fake.word().capitalize(),
        description = fake.text(max_nb_chars=100),
        category = choice(models.Category.objects.all()),
        brand = choice(models.Brand.objects.all()),
        is_active = fake.boolean(),
        is_featured = fake.boolean(),
        discount_percentage = round(random.uniform(10, 90)),
        updated_at = fake.date_this_month(),
    )
    product_base.save()
models.ProductBase.objects.all()
print('Add Base Products')


prduct_images = [
    '/product1_2.jpg', 
    '/product1.jpg',
    '/product2_2.jpg', 
    '/product2.jpg',
    '/product3_2.jpg', 
    '/product3.jpg'
]


for _ in range(20):
    product_variant = models.ProductVariant.objects.create(
        product_base = choice(models.ProductBase.objects.all()),
        name = fake.word().capitalize(),
        image = random.choice(prduct_images),
        price = round(random.uniform(100, 90)),
        stock_quantity = round(random.uniform(1, 30)),
    )
    product_variant.save()
models.ProductVariant.objects.all()
print('Add Product Variants')



