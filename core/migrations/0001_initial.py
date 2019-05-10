# Generated by Django 2.2.1 on 2019-05-10 12:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('ng', models.CharField(max_length=1)),
                ('img', models.URLField(null=True)),
                ('link_off', models.URLField()),
                ('energy', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('fat', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('saturated_fat', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('carbohydrate', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('sugars', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('proteins', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('salt', models.DecimalField(decimal_places=4, max_digits=6, null=True)),
                ('users', models.ManyToManyField(related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
