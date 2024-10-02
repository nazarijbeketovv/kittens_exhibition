# Generated by Django 5.1.1 on 2024-10-02 00:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Kitten',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(choices=[('black', 'Black'), ('white', 'White'), ('brown', 'Brown'), ('grey', 'Grey'), ('mixed', 'Mixed')], max_length=10)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to=settings.AUTH_USER_MODEL)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to='kittens.breed')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('kitten', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='kittens.kitten')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('kitten', 'user')},
            },
        ),
    ]
