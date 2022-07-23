from django.contrib.gis.db import models
from authe.models import Alborz

#
class AlborzUrban(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE , related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_urban'


class AlborzBare(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_bare'


class AlborzTree(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)
    # region =

    class Meta:
        managed = False
        db_table = 'alborz_tree'


class AlborzCropLand(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_cropland'


class AlborzRoad(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_road'


class AlborzGrass(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_grass'


class AlborzWater(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        managed = False
        db_table = 'alborz_water'

