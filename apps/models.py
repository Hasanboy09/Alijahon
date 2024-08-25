from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices, DateTimeField
from django.utils.text import slugify
from django_resized import ResizedImageField
from mptt.models import MPTTModel


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    class Role(TextChoices):
        ADMIN = "admin", 'Admin'
        OPERATOR = "operator", 'Operator'
        MANAGER = "manager", 'Manager'
        DRIVER = "driver", 'Driver'
        USER = "user", 'User'

    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone_number = models.CharField(max_length=12, unique=True)
    district = models.ForeignKey('apps.District', on_delete=models.CASCADE, related_name='users', null=True)

    @property
    def wishlist_all(self):
        return self.wishlists.values_list('product_id', flat=True)


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey('apps.Region', on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelSlug(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True  # o`zi table bo1lib yaratilmasligi kerak # noqa

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Category(BaseModel, BaseModelSlug):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Product(BaseModel, BaseModelSlug):
    description = RichTextUploadingField()
    price = models.FloatField()
    payment = models.FloatField()
    for_stream_price = models.FloatField(default=1000)
    category = models.ForeignKey('apps.Category', on_delete=models.CASCADE, to_field='slug', related_name='products')
    quantity = models.IntegerField()
    tg_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = ResizedImageField(size=[200, 200], quality=100, upload_to='products/')
    product = models.ForeignKey('apps.Product', on_delete=models.CASCADE, related_name='images')


class Order(BaseModel):
    class StatusType(TextChoices):
        NEW = "new", 'New'
        READY = "ready", 'Ready'
        DELIVER = "deliver", 'Deliver'
        DELIVERED = "delivered", 'Delivered'
        CANT_PHONE = "cant_phone", 'Cant_phone'
        CANCELED = "canceled", 'Canceled'
        ARCHIVED = 'archived', 'Archived'

    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=50, choices=StatusType.choices, default=StatusType.NEW)
    user = models.ForeignKey('apps.User', models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    stream = models.ForeignKey('apps.Stream', models.SET_NULL, null=True, blank=True, related_name='orders')
    phone_number = models.CharField(max_length=25)


class Wishlist(BaseModel):
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='wishlists', to_field='slug')
    user = models.ForeignKey('apps.User', models.CASCADE, related_name='wishlists')


class Stream(BaseModel):  # noqa
    name = models.CharField(max_length=255)
    discount = models.FloatField()
    count = models.IntegerField(default=0)
    product = models.ForeignKey('apps.Product', models.SET_NULL, null=True, related_name='streams')
    owner = models.ForeignKey('apps.User', models.CASCADE, related_name='streams')

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class SiteSettings(BaseModel):
    deliver_price = models.FloatField(default=0)
    site_photo = models.ImageField(upload_to='images/')
    start_time = DateTimeField()
    end_time = DateTimeField()


class NewOrder(Order):
    class Meta:
        proxy = True
        verbose_name = 'New Order'
        verbose_name_plural = 'News Orders'
