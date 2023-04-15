# Generated by Django 4.2 on 2023-04-15 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_verifydocument_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dedicatedperson',
            name='id_upload',
            field=models.ImageField(null=True, upload_to='data/ids/'),
        ),
        migrations.AlterField(
            model_name='verifydocument',
            name='proof_address',
            field=models.FileField(upload_to='data/address_proof/'),
        ),
        migrations.AlterField(
            model_name='verifydocument',
            name='tin_certificate',
            field=models.FileField(upload_to='data/tin_certificate/'),
        ),
        migrations.AlterField(
            model_name='verifydocument',
            name='trade_license',
            field=models.FileField(upload_to='data/trade_license/'),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]