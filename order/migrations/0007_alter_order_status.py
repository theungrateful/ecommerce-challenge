# Generated by Django 3.2.9 on 2022-02-28 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('p', 'pending'), ('c', 'completed'), ('x', 'cancelled')], default='p', max_length=10),
        ),
    ]
