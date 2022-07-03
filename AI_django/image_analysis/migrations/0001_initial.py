# Generated by Django 3.2.13 on 2022-06-22 11:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alborz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_nam', models.CharField(max_length=20, null=True)),
                ('center', models.CharField(max_length=20, null=True)),
                ('bakhsh', models.CharField(max_length=20, null=True)),
                ('shahrestan', models.CharField(max_length=20, null=True)),
                ('ostan', models.CharField(max_length=20, null=True)),
                ('area', models.FloatField(null=True)),
                ('hectares', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=32639)),
            ],
            options={
                'db_table': 'authe_alborz',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AlborzWater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_water',
            },
        ),
        migrations.CreateModel(
            name='AlborzUrban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_urban',
            },
        ),
        migrations.CreateModel(
            name='AlborzTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_tree',
            },
        ),
        migrations.CreateModel(
            name='AlborzRoad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_road',
            },
        ),
        migrations.CreateModel(
            name='AlborzGrass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_grass',
            },
        ),
        migrations.CreateModel(
            name='AlborzCropLand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_cropland',
            },
        ),
        migrations.CreateModel(
            name='AlborzBare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='image_analysis.alborz')),
            ],
            options={
                'db_table': 'alborz_bare',
            },
        ),
    ]
