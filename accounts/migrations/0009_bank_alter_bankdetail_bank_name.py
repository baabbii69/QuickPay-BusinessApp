# Generated by Django 4.2 on 2023-04-16 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='bankdetail',
            name='bank_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to='accounts.bank'),
        ),
    ]