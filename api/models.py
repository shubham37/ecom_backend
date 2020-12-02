from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone



class State(models.Model):
    state_name = models.CharField(max_length=48)

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=48)

    def __str__(self):
        return self.city_name


class Pincode(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)


# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.email)


class Contact(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=20, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    date_joined = models.DateField(verbose_name='date of query', auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Role:
    SELLER = 0
    BUYER = 1
    ADMIN = 2

ROLE_CHOICES = [
    (Role.SELLER, 'Seller'),
    (Role.BUYER, 'Buyer'),
    (Role.ADMIN, 'Admin')
]


class UserManager(BaseUserManager):

    def create_user(self, email, password="default"):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        # if not username:
        #     raise ValueError('Users must have username')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.role = Role.ADMIN
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    number = models.CharField(verbose_name='Mobile', max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=Role.BUYER)
 
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.role == Role.ADMIN

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()



# CACHE_DEFAULT_TIMEOUT = 60 * 60 * 24 # 1 day default (in secs)
# CACHE_CONFIG = {
#     'CACHE_TYPE': 'redis',
#     'CACHE_DEFAULT_TIMEOUT': CACHE_DEFAULT_TIMEOUT,
#     'CACHE_KEY_PREFIX': 'superset_',
#     'CACHE_REDIS_URL': 'redis://localhost:6379/1'
# }

# DATA_CACHE_CONFIG = CACHE_CONFIG

# 1. Create redis server
# 2. Uska url  CACHE_REDIS_URL isme pass krni hai
# 3. docker restart and done