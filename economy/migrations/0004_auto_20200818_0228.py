# Generated by Django 3.1 on 2020-08-18 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0003_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='commodity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='economy.commodity'),
        ),
    ]
