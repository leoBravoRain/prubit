# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-21 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prendas', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteGarments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('garment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prendas.Garment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='ForTryOnGarmentPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('photo', models.ImageField(upload_to='images/ForTryOnGarmentPhoto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='ForTryOnGarmentPhotoCurrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='miCuenta.ForTryOnGarmentPhoto')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('photo', models.ImageField(upload_to='images/profile')),
                ('currentProfilePhoto', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
    ]
