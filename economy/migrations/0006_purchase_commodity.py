# Generated by Django 3.1 on 2020-08-18 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0005_remove_purchase_commodity'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='commodity',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='economy.commodity'),
        ),
    ]
