# Generated by Django 4.2 on 2023-05-15 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_verifydocument_user_userwithbusinesstype'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifydocument',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verify_document', to=settings.AUTH_USER_MODEL),
        ),
    ]
