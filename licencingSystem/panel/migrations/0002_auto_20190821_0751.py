# Generated by Django 2.2.4 on 2019-08-21 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='panel.Plan'),
        ),
    ]