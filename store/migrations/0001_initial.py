# Generated by Django 3.1 on 2024-08-14 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_auto_20240810_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Product Name')),
                ('title', models.CharField(max_length=70, verbose_name='Product Title')),
                ('slug', models.SlugField(verbose_name='Product Slug')),
                ('description', models.TextField(verbose_name='Long Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Product Price')),
                ('discount', models.IntegerField(blank=True, null=True, verbose_name='Product Discount')),
                ('image', models.ImageField(upload_to='photos/product', verbose_name='Product Image')),
                ('stock', models.PositiveIntegerField(verbose_name='Remaining in Stock')),
                ('available', models.BooleanField(default=True, verbose_name='Is Available in Stock')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='Product Category')),
            ],
        ),
    ]
