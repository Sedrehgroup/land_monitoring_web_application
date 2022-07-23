from django.contrib.gis.db import models
from django.utils.timezone import now


class Alborz(models.Model):
    per_nam = models.CharField(max_length=20, null=True)
    center = models.CharField(max_length=20, null=True)
    bakhsh = models.CharField(max_length=20, null=True)
    shahrestan = models.CharField(max_length=20, null=True)
    ostan = models.CharField(max_length=20, null=True)
    area = models.FloatField(null=True)
    hectares = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=32639)

    class Meta:
        managed = False
        db_table = 'authe_alborz'


class AlborzUrban(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE , related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_urban'


class AlborzBare(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_bare'


class AlborzTree(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)
    # region =

    class Meta:
        db_table = 'alborz_tree'


class AlborzCropLand(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_cropland'


class AlborzRoad(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_road'


class AlborzGrass(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_grass'


class AlborzWater(models.Model):
    date = models.DateField()
    area = models.FloatField()
    region = models.ForeignKey(Alborz, on_delete=models.CASCADE, related_name='+')
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'alborz_water'

