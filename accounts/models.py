from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import uuid
from django.contrib.auth import get_user_model

staff_sizes = (
("1-5 People", "1-5 People"), ("5-10 People", "5-10 People"), ("More Than 10 People", "More Than 10 People"))
Transaction_Volume = (("10,000 - 100,000", "10,000 - 100,000"), ("100,000 - 500,000", "100,000 - 500,000"),
                      ("More Than 500,000", "More Than 500,000"))
genders = (("Male", "Male"), ("Female", "Female"))
id_type = (("Passport", "Passport"), ("Driver License", "Driver License"), ("kebele ID", "kebele ID"),
           ("National ID", "National ID"))


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not email:
            raise ValueError("Email field is required")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email Field is required to open an Account')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user


class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user}'s balance: {self.balance}"


class ConnectedBankss(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    is_verified = models.BooleanField(default=False)
    bank_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='connected_banks', null=True
    )

    def __str__(self):
        return self.name


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255, unique=True)
    business_type = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'business_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class UserWithBusinessType(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='user_with_business_type')
    business_type = models.CharField(max_length=255, null=True)


class BankDetail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bank_detail'
    )
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.account_name}'


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    bank = models.ForeignKey(ConnectedBankss, on_delete=models.CASCADE, related_name='transactions', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Transaction #{self.pk}'


class Industry(models.Model):
    industry_name = models.CharField(max_length=255)

    def __str__(self):
        return self.industry_name


class Incorporation(models.Model):
    incorp_name = models.CharField(max_length=255)

    def __str__(self):
        return self.incorp_name


class States(models.Model):
    state_name = models.CharField(max_length=255)

    def __str__(self):
        return self.state_name


class StaffSize(models.Model):
    staff_sizes = models.CharField(max_length=255)

    def __str__(self):
        return self.staff_sizes


class TransVolume(models.Model):
    trans_volume = models.CharField(max_length=255)

    def __str__(self):
        return self.trans_volume


class DedicatedPerson(models.Model):
    gender = models.CharField(max_length=15, choices=genders)
    date_of_birth = models.DateField()
    full_address = models.CharField(max_length=100, null=True)
    state = models.ForeignKey(States, on_delete=models.PROTECT, related_name="state", null=False)
    ids = models.CharField(max_length=20, choices=id_type, null=False)
    id_upload = models.ImageField(upload_to='data/ids/', null=False)


class VerifyDocument(models.Model):
    business_type = models.BooleanField(default=True)
    is_utility = models.BooleanField(default=False)
    industrys = models.ForeignKey(Industry, on_delete=models.PROTECT, related_name="industrys")
    category = models.CharField(max_length=30)
    staff_size = models.CharField(max_length=30, choices=staff_sizes)
    trans_volume = models.CharField(max_length=30, choices=Transaction_Volume)
    legal_BN = models.CharField(max_length=50, null=False)
    tin_numbers = models.CharField(max_length=50, null=False)
    vat_check = models.BooleanField(default=False)
    business_reg_num = models.CharField(max_length=30)
    incorp_type = models.ForeignKey(Incorporation, on_delete=models.PROTECT, related_name="incorporation_name")
    trade_license = models.FileField(upload_to='data/trade_license/')
    tin_certificate = models.FileField(upload_to='data/tin_certificate/')
    memorandum = models.FileField(upload_to='data/memorandum/')
    business_contact = models.CharField(max_length=30)
    proof_address = models.FileField(upload_to='data/address_proof/')
    states = models.ForeignKey(States, on_delete=models.PROTECT, related_name="states")
    kifle_ketema = models.CharField(max_length=25)
    woreda = models.CharField(max_length=20)
    kebele = models.CharField(max_length=5)
    house_number = models.CharField(max_length=20)
    frendly_BN = models.CharField(max_length=50)
    business_phone = models.CharField(max_length=12)
    business_email = models.EmailField(max_length=255, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                related_name='verify_document')

    def __str__(self):
        return self.legal_BN


# class BillType(models.Model):
#     name = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#
#     def __str__(self):
#         return f'{self.name} - {self.amount}'
#
#
# class Customer(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#         unique=True
#     )
#     fname = models.CharField(max_length=255)
#     lname = models.CharField(max_length=255)
#
#     def __str__(self):
#         return f'{self.fname} - {self.lname}'
#
#
# class Utility(models.Model):
#     user = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return f'{self.name} - {self.name}'
#
#
# class UtilityNormal(models.Model):
#     utility = models.ForeignKey(Utility, on_delete=models.CASCADE, related_name='utility', null=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer', null=True)
#     bill_type = models.CharField(max_length=255, null=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-timestamp']
#
#     def __str__(self):
#         return f'{self.utility.name} - {self.customer}'
