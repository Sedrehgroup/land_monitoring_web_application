import os
import rasterio
import numpy as np
from rasterio.features import shapes
from shapely.geometry import Polygon
from shapely.ops import unary_union
from django.contrib.gis.geos import GEOSGeometry


class Change:
    def __init__(self, geom_id, before_name, after_name, path):
        self.geom_id = geom_id
        self.before_name = before_name
        self.after_name = after_name
        self.path = path
        self.before_dataset = None
        self.after_dataset = None
        self.shape = None

    def get_datasets(self):
        ai_images = os.path.join(self.path, 'images/alborz', str(self.geom_id))
        before_image_path = os.path.join(ai_images, self.before_name)
        after_image_path = os.path.join(ai_images, self.after_name)

        self.before_dataset = rasterio.open(before_image_path)
        self.after_dataset = rasterio.open(after_image_path)
        print('done')

    def change_analysis(self):
        classes = {"1": 'Tree', "2": 'Barren', "3": 'Grassland', "4": 'Cropland', "5": 'Built-up', "7": 'water'}

        before_raster = self.before_dataset.read(1)
        after_raster = self.after_dataset.read(1)

        before_raster_flatten = before_raster.flatten()
        after_raster_flatten = after_raster.flatten()
        # because we have not second picture
        np.random.shuffle(after_raster_flatten)
        self.shape = before_raster.shape

        change_array = []
        for i in range(len(after_raster_flatten)):
            if before_raster_flatten[i] == after_raster_flatten[i]:
                change_array.append('not_changed')
            elif before_raster_flatten[i] == 0 or after_raster_flatten[i] == 0:
                change_array.append('no_data')
            else:
                change_array.append(f'from_{classes[str(before_raster_flatten[i])]}_to_{classes[str(after_raster_flatten[i])]}')

        unique, counts = np.unique(change_array, return_counts=True)
        result = np.column_stack((unique, counts))[:-2]
        return result, change_array

    def get_polygons(self, class_change):
        geom = []
        _, change_array = self.change_analysis()
        mask = np.where(np.array(change_array) == class_change, 1, 0).astype('int16')
        mask = np.reshape(mask, self.shape)

        for i, (s, v) in enumerate(shapes(mask, mask=None, transform=self.before_dataset.transform)):
            if v == 1:
                # geom.append(Polygon(s['coordinates'][0]))
                geom.append(s['coordinates'][0])
        # geom = unary_union(geom)
        return geom



