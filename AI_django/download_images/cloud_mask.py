import os
from glob import glob
import rasterio
import cv2
import numpy as np
import shutil


def apply_mask(tci_image, cloud_image, transform, cloud_masked_path, background_path):

    sentinel_image = rasterio.open(tci_image)
    sentinel = sentinel_image.read()
    metadata = sentinel_image.meta.copy()

    cloud_image = rasterio.open(cloud_image)

    mask = cloud_image.read()[0]
    mask = cv2.resize(mask, (10980, 10980), interpolation=cv2.INTER_AREA)
    mask = mask < 50

    # turn zero values to nan values

    out = mask.astype(sentinel.dtype)
    # apply mask on sentinel bands
    for i in range(len(sentinel)):
        down_scale_sentinel = cv2.resize(sentinel[i], (10980, 10980), interpolation=cv2.INTER_AREA)
        height = down_scale_sentinel.shape[0]
        width = down_scale_sentinel.shape[1]
        os.chdir(cloud_masked_path)

        image_name = tci_image.split('.')[0]
        metadata.update({'count': 1, 'height': height, 'width': width, 'transform': transform})
        with rasterio.open(image_name + str(i) + '_cloud_masked.jp2', 'w', **metadata) as reprojected:
            reprojected.write(np.array([out * down_scale_sentinel]))

        os.chdir(background_path)


def cloud_mask(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    background_path = os.path.join(path, 'images/background_images')

    if not os.path.isdir(cloud_masked_path):
        os.mkdir(cloud_masked_path)
    os.chdir(background_path)

    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    for tile in tiles:
        tile_cloud_images = sorted(glob(f'*_{tile}*'))
        print('tile_cloud_images', tile_cloud_images)
        tile_images = sorted(glob(f'{tile}*'))
        print('tile_images', tile_images)
        dataset = rasterio.open(tile_images[0])
        transform = dataset.transform

        final_tile_images = []
        for k in range(len(tile_cloud_images)):
            final_tile_images.append(tile_images[k*11:(k+1)*11])
        print('final_tile_images', final_tile_images)

        for i in range(len(tile_cloud_images)):
            for j in range(len(final_tile_images[i])):
                apply_mask(tci_image=final_tile_images[i][j], cloud_image=tile_cloud_images[i], transform=transform ,cloud_masked_path=cloud_masked_path, background_path=background_path)
                print('mask applied')

    shutil.rmtree(background_path)