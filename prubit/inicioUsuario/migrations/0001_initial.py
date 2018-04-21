# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-21 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('inicioEmpresa', '0001_initial'),
        ('probador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentTestedGarmentPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('creationDate', models.DateField()),
                ('likeCount', models.IntegerField(default=0)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='probador.TestedGarmentPhoto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyLikeToUserCommentToGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyUserFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='1_friend+', to='usuarios.UserSite')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='2_friend+', to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='FriendInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='1_friend+', to='usuarios.UserSite')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='2_friend+', to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='LikeTestedGarmentPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateField()),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='probador.TestedGarmentPhoto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='LikeToCommentOfTestedPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioUsuario.CommentTestedGarmentPhoto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='LikeToGarmentPostOfCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('garmentCompanyPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioEmpresa.GarmentCompanyPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='RecuperacionPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visto', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='UserCommentToGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('creationDate', models.DateTimeField()),
                ('likeCount', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioEmpresa.GarmentCompanyPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='UserLikeToCompanyCommentToGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioEmpresa.CompanyCommentToGarmentCompanyPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.CreateModel(
            name='UserLikeToUserCommentOfGarmentCompanyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationDate', models.DateTimeField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioUsuario.UserCommentToGarmentCompanyPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.UserSite')),
            ],
        ),
        migrations.AddField(
            model_name='companyliketousercommenttogarmentcompanypost',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioUsuario.UserCommentToGarmentCompanyPost'),
        ),
        migrations.AddField(
            model_name='companyliketousercommenttogarmentcompanypost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Company'),
        ),
    ]
