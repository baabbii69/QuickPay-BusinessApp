# Generated by Django 4.2 on 2023-05-05 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('business_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('business_name', models.CharField(max_length=255, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConnectedBankss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('bank_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='connected_banks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Incorporation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorp_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_type', models.BooleanField(default=True)),
                ('category', models.CharField(max_length=30)),
                ('staff_size', models.CharField(choices=[('1-5 People', '1-5 People'), ('5-10 People', '5-10 People'), ('More Than 10 People', 'More Than 10 People')], max_length=30)),
                ('trans_volume', models.CharField(choices=[('10,000 - 100,000', '10,000 - 100,000'), ('100,000 - 500,000', '100,000 - 500,000'), ('More Than 500,000', 'More Than 500,000')], max_length=30)),
                ('legal_BN', models.CharField(max_length=50)),
                ('tin_numbers', models.CharField(max_length=50)),
                ('vat_check', models.BooleanField(default=False)),
                ('business_reg_num', models.CharField(max_length=30)),
                ('trade_license', models.FileField(upload_to='data/trade_license/')),
                ('tin_certificate', models.FileField(upload_to='data/tin_certificate/')),
                ('memorandum', models.FileField(upload_to='data/memorandum/')),
                ('business_contact', models.CharField(max_length=30)),
                ('proof_address', models.FileField(upload_to='data/address_proof/')),
                ('kifle_ketema', models.CharField(max_length=25)),
                ('woreda', models.CharField(max_length=20)),
                ('kebele', models.CharField(max_length=5)),
                ('house_number', models.CharField(max_length=20)),
                ('frendly_BN', models.CharField(max_length=50)),
                ('business_phone', models.CharField(max_length=12)),
                ('business_email', models.EmailField(max_length=255, unique=True)),
                ('incorp_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incorporation_name', to='accounts.incorporation')),
                ('industrys', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='industrys', to='accounts.industry')),
                ('states', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='states', to='accounts.states')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.connectedbankss')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='DedicatedPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=15)),
                ('date_of_birth', models.DateField()),
                ('full_address', models.CharField(max_length=100, null=True)),
                ('ids', models.CharField(choices=[('Passport', 'Passport'), ('Driver License', 'Driver License'), ('kebele ID', 'kebele ID'), ('National ID', 'National ID')], max_length=20)),
                ('id_upload', models.ImageField(upload_to='data/ids/')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='state', to='accounts.states')),
            ],
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_detail', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
