from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class UserAuthManager(BaseUserManager):
    """
    Requires email address instead of username.
    Required Functions:
        _create_user
        create_user
        create_superuser
    """
    def _create_user(self,email,password,is_staff,is_superuser,**extra_fields):
        # save login time
        log_time = timezone.now()

        if not email:
            raise ValueError('Email not provided')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=log_time,
                          date_joined=log_time,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password=None,**extra_fields):
        return self._create_user(email,password,False,False,**extra_fields)

    def create_superuser(self,email,password,**extra_fields):
        return self._create_user(email,password,True,True,**extra_fields)

class UserAuth(AbstractBaseUser, PermissionsMixin):

    email = models.CharField(max_length=64,unique=True)
    # meta fields. Do not modify from client side.
    date_joined = models.DateTimeField(_('date joined'),default = timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserAuthManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.email)

    def get_absolute_url(self):
        return 'accounts/%s/'%urlquote(self.email)

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass