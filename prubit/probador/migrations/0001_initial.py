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
            name='TestedGarmentPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images/TestedGarmentPhoto')),
                ('likeCount', models.IntegerField(default=0)),
                ('ownComment', models.CharField(max_length=300, null=True)),
                ('creationDate', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='TestedGarmentPhoto_Garment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prendas.Garment')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='probador.TestedGarmentPhoto')),
            ],
        ),
    ]
