import os
from glob import glob
import rasterio
import numpy as np
from rasterio.windows import Window
from torch_semi_seg_model.Final_Product import semi_seg_product


def median_images(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    os.chdir(cloud_masked_path)

    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    bands = ['B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B11', 'B12', 'TCI_10m0', 'TCI_10m1', 'TCI_10m2']
    tci_bands = ['TCI_10m0', 'TCI_10m1', 'TCI_10m2']

    print('starting combine images')
    for tile in tiles:
        for band in bands:
            tile_images = glob(tile+'*'+band+'*')
            print(tile_images)
            raster = []
            for image in tile_images:
                dataset = rasterio.open(image)
                metadata = dataset.meta.copy()
                raster.append(dataset.read()[0])

            if band in tci_bands:
                median_raster = np.median(raster, axis=0).astype('uint8')
            else:
                median_raster = np.median(raster, axis=0).astype('uint16')
            print('median_raster', median_raster)
            with rasterio.open(f'{tile}_{band}_median.jp2', 'w', **metadata) as tile_dataset:
                tile_dataset.write(np.array([median_raster]))

        print('median_images')

    original_files = glob('*')
    for file in original_files:
        if not file.endswith('median.jp2'):
            os.remove(file)


def split_2d(array, splits):
    x, y = splits
    return np.split(np.concatenate(np.split(array, y, axis=1)), x*y)


def AI_image_preparation(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    ai_image_path = os.path.join(path, 'images/AI_image')
    if not os.path.isdir(ai_image_path):
        os.mkdir(ai_image_path)

    os.chdir(cloud_masked_path)
    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    bands = ['B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B11', 'B12', 'TCI_10m0', 'TCI_10m1', 'TCI_10m2']
    for tile in tiles:
        for band in bands:
            image_path = f'{tile}_{band}_median.jp2'
            band_dataset = rasterio.open(image_path)
            band_metadata = band_dataset.meta.copy()

            band_raster = band_dataset.read()[0]
            split_raster = split_2d(band_raster, (30, 20))

            height = split_raster[0].shape[0]
            width = split_raster[0].shape[1]
            x_origin, y_origin = 0, 0

            window = Window(x_origin, y_origin, height, width)
            transform = band_dataset.window_transform(window)

            band_metadata.update({'height': height, 'width': width, 'transform': transform})

            os.chdir(ai_image_path)
            for i in range(20*30):
                with rasterio.open(f'{i}_{tile}_{band}.jp2', 'w', **band_metadata) as tile_dataset:
                    tile_dataset.write(np.array([split_raster[i]]))
            print(f'{tile}_{band}.jp2')
            os.chdir(cloud_masked_path)


def run_model(path):
    semi_seg_product(path=path)

