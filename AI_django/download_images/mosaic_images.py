import os
from glob import glob
import rasterio
import numpy as np
from rasterio.merge import merge
from rasterio.mask import mask
import fiona
from rasterio.warp import calculate_default_transform, reproject
from utils import LayerAdd
import shutil


def stack_2d(array, splits):
    x, y = splits
    return np.hstack(np.split(np.vstack(array), y, axis=0))


def mosaic_labels(path):
    alborz_path = os.path.join(path, 'images/alborz')
    ai_image_path = os.path.join(path, 'images/AI_image')
    if not os.path.isdir(alborz_path):
        os.mkdir(alborz_path)

    ai_label_path = os.path.join(path, 'images/AI_Result')

    os.chdir(ai_label_path)
    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']
    for tile in tiles:
        tile_label = []
        label_images = []
        for i in range(600):
            label_images.append(f'product_{i}_{tile}.tif')
        for image in label_images:
            dataset = rasterio.open(image)
            transform = dataset.transform
            raster = dataset.read()
            crs = dataset.crs
            tile_label.append(np.array(raster[0]))

        stacked_tile_label = stack_2d(tile_label, (30, 20))
        stacked_tile_label[stacked_tile_label == 10] = 0
        # turn snow imdex to bare land
        stacked_tile_label[stacked_tile_label == 6] = 0
        stacked_tile_label[stacked_tile_label == 9] = 1
        stacked_tile_label[stacked_tile_label == 8] = 7
        stacked_tile_label[stacked_tile_label == 2] = 3
        stacked_tile_label[stacked_tile_label == 0] = 2

        unique, counts = np.unique(stacked_tile_label, return_counts=True)
        result = np.column_stack((unique, counts))
        print(result)

        os.chdir(alborz_path)
        new_dataset = rasterio.open(f"{tile}_label_median.tif", 'w', driver='GTiff',
                                    height=10980, width=10980,
                                    count=1, dtype=str(stacked_tile_label.dtype),
                                    crs=crs,
                                    transform=transform)
        new_dataset.write(np.array([stacked_tile_label]))
        os.chdir(ai_label_path)

    if os.path.exists(ai_image_path):
        shutil.rmtree(ai_image_path)

    if os.path.exists(ai_label_path):
        shutil.rmtree(ai_label_path)


def stack_tci_files(path):
    cloud_masked_path = os.path.join(path, 'images/cloud_masked_images')
    alborz_path = os.path.join(path, 'images/alborz')
    if not os.path.isdir(alborz_path):
        os.mkdir(alborz_path)
    os.chdir(cloud_masked_path)

    print('glob median images')
    tiles = ['T39SVV', 'T39SVA', 'T39SWV', 'T39SWA']

    for tile in tiles:
        final_tci = []
        median_src = sorted(glob(f'{tile}_TCI*'))
        for tci in median_src:
            dataset = rasterio.open(tci)
            metadata = dataset.meta.copy()
            final_tci.append(dataset.read()[0])

            metadata.update({'count': len(final_tci)})
            os.chdir(alborz_path)
            with rasterio.open(f'alborz_TCI_{tile}_median.jp2', 'w', **metadata) as tile_dataset:
                tile_dataset.write(np.array(final_tci))

            os.chdir(cloud_masked_path)
        print(f'RGB image of tile {tile} is created')

    if os.path.exists(cloud_masked_path):
        shutil.rmtree(cloud_masked_path)


def mosaic_tiles(images, name):
    src_files_to_mosaic = []
    for fp in images:
        src = rasterio.open(fp)
        metadata = src.meta.copy()
        src_files_to_mosaic.append(src)

    print('src_files_to_mosaic', src_files_to_mosaic)
    mosaic, out_trans = merge(src_files_to_mosaic)
    metadata.update({'transform': out_trans, 'width': mosaic.shape[2], 'height': mosaic.shape[1]})

    with rasterio.open(f'alborz_{name}_median.jp2', 'w', **metadata) as tile_dataset:
        tile_dataset.write(np.array(mosaic))


def mosaic_alborz_tiles(path):
    alborz_path = os.path.join(path, 'images/alborz')
    os.chdir(alborz_path)

    tci_images = glob('*TCI*')
    label_images = glob('*label*')

    mosaic_tiles(images=tci_images, name='TCI')
    mosaic_tiles(images=label_images, name='label')

    for image in tci_images:
        os.remove(image)

    for image in label_images:
        os.remove(image)


def turn_jp2_tiff(jp2_dataset, path):
    target_crs = 'EPSG:4326'
    transform, width, height = calculate_default_transform(jp2_dataset.crs, target_crs, jp2_dataset.width,
                                                           jp2_dataset.height,
                                                           *jp2_dataset.bounds)
    metadata = jp2_dataset.meta.copy()
    metadata.update({'driver': 'GTiff', 'crs': target_crs, 'transform': transform, 'width': width, 'height': height})

    with rasterio.open(path, 'w', **metadata) as reprojected:
      for band in range(1, jp2_dataset.count + 1):
          reproject(
              source=rasterio.band(jp2_dataset, band),
              destination=rasterio.band(reprojected, band),
              src_transform=jp2_dataset.transform,
              src_crs=jp2_dataset.crs,
              dst_transform=transform,
              dst_crs=target_crs
          )


def crop_images(path, time=14012):
    alborz_path = os.path.join(path, 'images/alborz')
    aoi_file = fiona.open(os.path.join(path, 'shape_files/alborz.shp'))
    aoi_file_province = fiona.open(os.path.join(path, 'shape_files/Palborz.shp'))

    os.chdir(alborz_path)
    images = glob('*_median.jp2')
    for image in images:
        image_name = image.split('_')[1]
        dataset = rasterio.open(image)
        for i in range(len(aoi_file)):
            geometry = [aoi_file[i]['geometry']]
            per_name = [aoi_file[i]['properties']['PER_NAM']]
            print(per_name, ':', i)

            out_meta = dataset.meta.copy()
            out_image, out_transform = mask(dataset, geometry, crop=True)
            out_meta.update({"height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform})

            directory_path = os.path.join(alborz_path, str(i+1))
            if not os.path.isdir(directory_path):
                os.mkdir(directory_path)

            out_raster = rasterio.open(os.path.join(directory_path, f'{image_name}_{time}.jp2'), 'w', **out_meta)
            out_raster.write(out_image)

            # turn jp2 to tiff file
            tiff_path = os.path.join(directory_path, f'{image_name}_{time}.tiff')
            turn_jp2_tiff(jp2_dataset=out_raster, path=tiff_path)

            if image_name == 'label':
                os.remove(os.path.join(directory_path, f'{image_name}_{time}.jp2'))

        out_meta = dataset.meta.copy()
        geometry = [aoi_file_province[0]['geometry']]

        out_image, out_transform = mask(dataset, geometry, crop=True)
        out_meta.update({"height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        province_path = os.path.join(alborz_path, 'province')
        if not os.path.isdir(province_path):
            os.mkdir(province_path)

        out_raster = rasterio.open(os.path.join(province_path, f'{image_name}_{time}.jp2'), 'w', **out_meta)
        out_raster.write(out_image)

        tiff_path = os.path.join(province_path, f'{image_name}_{time}.tiff')
        turn_jp2_tiff(jp2_dataset=out_raster, path=tiff_path)

        if image_name == 'label':
            os.remove(os.path.join(province_path, f'{image_name}_{time}.jp2'))

        list_images = [str(item + 1) for item in range(30)]
        list_images.append("province")
        LayerAdd(filename=f'{image_name}_{time}.tiff', region_id=list_images, province='alborz').tif_add()

        os.remove(image)