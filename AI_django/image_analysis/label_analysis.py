import os
import numpy as np
from django.conf import settings
import rasterio
from rasterio.features import shapes
from shapely.geometry import Polygon
from shapely.ops import unary_union
from .models import AlborzUrban, AlborzBare, AlborzRoad, AlborzTree, AlborzWater, AlborzGrass, AlborzCropLand , Alborz
import datetime
from django.contrib.gis.geos import GEOSGeometry
import geopandas


classify_index = {
    "1": AlborzTree,
    "2": AlborzBare,
    "3": AlborzGrass,
    "4": AlborzCropLand,
    "5": AlborzUrban,
    "7": AlborzWater
}


class Raster2Vec:
    def __init__(self, filename):
        self.filename = filename
        self.raster = None
        self.dataset = None
        self.mask = None

    def __call__(self):
        with rasterio.Env():
            with rasterio.open(self.filename) as dataset:
                self.dataset = dataset
                self.raster = self.dataset.read(1)

    def run(self, value):
        geom = []
        mask = None
        for i, (s, v) in enumerate(shapes(self.raster, mask=mask, transform=self.dataset.transform)):
            if v == float(value):
                print(s)
                geom.append((Polygon(s['coordinates'][0])))
        # geom = unary_union(geom)
        geom = geopandas.GeoSeries(geom)
        geom = geom.unary_union
        return str(geom)


def count_pixels(filename):
    result_images = os.path.join(settings.BASE_DIR)
    os.chdir(result_images)

    dataset = rasterio.open(filename)
    raster = dataset.read()
    raster_before_flatten = raster.flatten()

    unique, counts = np.unique(raster_before_flatten, return_counts=True)
    result = np.column_stack((unique, counts))
    return result


def record(date, filename, geom_id):
    year = int(date[:4])
    month = int(date[4:])
    print('year', year)
    print('month', month)
    model_date = datetime.date(year=year, month=month, day=1)

    # delete zero values of crop
    result = count_pixels(filename=filename)[1:]

    geomid = Alborz.objects.get(id=geom_id)
    get_geom = Raster2Vec(filename=filename)
    get_geom()
    # TODO : error for save a polygon occurs. we must replace try with another solution
    for item in result:
        try:
            index = item[0]
            count = item[1]
            geom = get_geom.run(index)
            model = classify_index[str(index)]()
            if not model.objects.filter(region = geom_id , date = model_date).exists():
                model.date = model_date
                model.area = count
                model.region = geomid
                model.geom = GEOSGeometry(str(geom))
                model.save()
        except:
            pass


def update_database(path, date):
    alborz_path = os.path.join(path, 'images/alborz')
    directories = [str(item + 1) for item in range(30)]

    for directory in directories:
        image_path = os.path.join(alborz_path, directory+f'/label_{date}.tiff')
        record(date=date, filename=image_path, geom_id=directory)
        print(image_path)
