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
            name='CompanyCommentToGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('creationDate', models.DateTimeField()),
                ('likeCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyLikeToCompanyCommentToGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioEmpresa.CompanyCommentToGarmentCompanyPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Company')),
            ],
        ),
        migrations.CreateModel(
            name='GarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('creationDate', models.DateTimeField()),
                ('likeCount', models.IntegerField(default=0)),
                ('garment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prendas.Garment')),
            ],
        ),
        migrations.AddField(
            model_name='companycommenttogarmentcompanypost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioEmpresa.GarmentCompanyPost'),
        ),
        migrations.AddField(
            model_name='companycommenttogarmentcompanypost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Company'),
        ),
    ]
