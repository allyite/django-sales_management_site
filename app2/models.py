from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, Permission, AbstractUser
)



class User1(AbstractUser):
    uaddr= models.CharField(blank=True, max_length=100)
    udob = models.DateField(null=True, blank=True)
    uemp= models.CharField(blank=True, max_length=100)
    
    class Meta:
        permissions = [
            ("mng_users", "manage users is_active etc"),
        ]

#----------------------------------------------------#

'''
class MyUserManager(BaseUserManager):
    def create_user(self, uname,uemail, password=None):
        if not uname or not uemail:
            raise ValueError('Please provide all mandatory fields')

        user = self.model(uname=uname,uemail=uemail)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uname,uemail ,password=None):

        user = self.create_user(
            uname=uname, uemail=uemail
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    uname= models.CharField(max_length=10,unique=True)
    uemail = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    ufname= models.CharField(max_length=20)
    ulname= models.CharField(max_length=20)
    uaddr= models.CharField(max_length=100)
    udob = models.DateField(null=True, blank=True)
    uemp= models.CharField(max_length=100) #user-employer

    user_permissions= models.ManyToManyField(Permission) 
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    
    objects = MyUserManager()

    USERNAME_FIELD = 'uname'
    REQUIRED_FIELDS = ['uemail']
    #USERNAME_FIELD & pwd : no need to mention / always prompted/reqd

    def __str__(self):
        return self.uname
    
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
'''
