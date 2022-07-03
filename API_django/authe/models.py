# from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# TODO : declare user fields
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):

        user = self.create_user(username, email='something@admin.com', password=password)
        user.is_admin = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    geom = models.ManyToManyField('Alborz')
    objects = UserManager()
    # REQUIRED_FIELDS = ['username' , 'email' , 'password']

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Alborz(models.Model):
    per_nam = models.CharField(max_length=20, null=True)
    center = models.CharField(max_length=20, null=True)
    bakhsh = models.CharField(max_length=20, null=True)
    shahrestan = models.CharField(max_length=20, null=True)
    ostan = models.CharField(max_length=20, null=True)
    area = models.FloatField(null=True)
    hectares = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=32639)
