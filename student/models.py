from django.db import models

# Create your models here.

from django.db import models

from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Define a dictionary to hold all roles for easy management
ROLES = {
    'STUDENT': 'Student',
    'FACULTY': 'Faculty',
    'HOD': 'HOD',
    'AO': 'AO',
    'DEAN': 'Dean',
    'DSW': 'DSW',
    'DIRECTOR': 'Director',
}

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', ROLES['DIRECTOR'])

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Use the dictionary to create the choices tuple for the model field
    ROLE_CHOICES = [
        (key, value) for key, value in ROLES.items()
    ]

    email = models.EmailField(_('email address'), unique=True)
    
    default_password = models.CharField(max_length=128, blank=True, null=True, 
                                        help_text=_("The initial default password for the user. This value should not change."))
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLES['STUDENT'],
        verbose_name=_('user role')
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'default_password'] 

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Student(models.Model):
    name = models.CharField(max_length=100, blank=False)
    gmail = models.EmailField(unique=True)
    id_no = models.IntegerField(unique=True, primary_key=True)
    class_year = models.IntegerField(default=0)
    
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
    ]
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, blank=True)

    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    hall_ticket_no = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=10, blank=False)
    parent_phone_number = models.CharField(max_length=10,blank=True)
    guardian = models.BooleanField(default=False)
    
    # Hostel information
    hostel_name = models.CharField(max_length=100, blank=True)
    room_no = models.CharField(max_length=10, blank=True)
    
    blood_group = models.CharField(max_length=5, blank=True)
    year = models.IntegerField()
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.gmail